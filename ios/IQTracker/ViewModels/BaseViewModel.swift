import Foundation
import Combine

/// Base class for ViewModels providing common functionality
class BaseViewModel: ObservableObject {
    @Published var isLoading: Bool = false
    @Published var error: Error?

    var cancellables = Set<AnyCancellable>()

    init() {}

    /// Handle errors and set them for display
    func handleError(_ error: Error) {
        self.isLoading = false
        self.error = error
    }

    /// Clear any existing error
    func clearError() {
        self.error = nil
    }

    /// Set loading state
    func setLoading(_ loading: Bool) {
        self.isLoading = loading
    }
}
