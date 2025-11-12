import Combine
import Foundation
import UIKit
import UserNotifications

/// ViewModel for managing notification settings
@MainActor
class NotificationSettingsViewModel: BaseViewModel {
    // MARK: - Published Properties

    /// Whether notifications are enabled in the backend
    @Published var notificationEnabled: Bool = false

    /// Whether system permission is granted
    @Published var systemPermissionGranted: Bool = false

    /// Whether we're currently checking permissions
    @Published var isCheckingPermission: Bool = false

    // MARK: - Private Properties

    private let notificationService: NotificationServiceProtocol
    private let authManager: AuthManager

    // MARK: - Initialization

    init(
        notificationService: NotificationServiceProtocol = NotificationService.shared,
        authManager: AuthManager = AuthManager.shared
    ) {
        self.notificationService = notificationService
        self.authManager = authManager
        super.init()
    }

    // MARK: - Public Methods

    /// Load current notification preferences
    func loadNotificationPreferences() async {
        setLoading(true)
        clearError()

        do {
            // Get backend preferences
            let response = try await notificationService.getNotificationPreferences()
            notificationEnabled = response.notificationEnabled

            // Check system permission
            await checkSystemPermission()

            setLoading(false)

        } catch {
            handleError(error) {
                await self.loadNotificationPreferences()
            }
        }
    }

    /// Toggle notification preferences
    func toggleNotifications() async {
        // Check system permission first
        await checkSystemPermission()

        // If user wants to enable but doesn't have permission, prompt them
        if !notificationEnabled && !systemPermissionGranted {
            await requestSystemPermission()
            return
        }

        // Update backend preference
        setLoading(true)
        clearError()

        do {
            let newValue = !notificationEnabled
            let response = try await notificationService.updateNotificationPreferences(enabled: newValue)
            notificationEnabled = response.notificationEnabled

            setLoading(false)

        } catch {
            handleError(error) {
                await self.toggleNotifications()
            }
        }
    }

    /// Check current system permission status
    func checkSystemPermission() async {
        isCheckingPermission = true

        let settings = await UNUserNotificationCenter.current().notificationSettings()
        systemPermissionGranted = settings.authorizationStatus == .authorized

        isCheckingPermission = false
    }

    /// Request system notification permission
    func requestSystemPermission() async {
        do {
            let granted = try await UNUserNotificationCenter.current()
                .requestAuthorization(options: [.alert, .sound, .badge])

            systemPermissionGranted = granted

            if granted {
                // Register for remote notifications
                await MainActor.run {
                    UIApplication.shared.registerForRemoteNotifications()
                }

                // Now enable in backend
                await toggleNotifications()
            }

        } catch {
            handleError(error)
        }
    }

    /// Open system settings for the app
    func openSystemSettings() {
        guard let settingsURL = URL(string: UIApplication.openSettingsURLString) else {
            return
        }

        if UIApplication.shared.canOpenURL(settingsURL) {
            UIApplication.shared.open(settingsURL)
        }
    }

    // MARK: - Computed Properties

    /// Whether the toggle should be enabled
    var canToggle: Bool {
        !isLoading && !isCheckingPermission
    }

    /// Status message to display
    var statusMessage: String? {
        if notificationEnabled && !systemPermissionGranted {
            return "Notifications are enabled but system permission is denied. Tap to open Settings."
        }
        return nil
    }

    /// Whether to show a warning about system permissions
    var showPermissionWarning: Bool {
        notificationEnabled && !systemPermissionGranted
    }
}
