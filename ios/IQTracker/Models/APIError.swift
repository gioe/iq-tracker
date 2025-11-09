import Foundation

/// Operation context for better error messages
enum NetworkOperation {
    /// User login operation
    case login
    /// User registration operation
    case register
    /// Fetching test questions
    case fetchQuestions
    /// Submitting test answers
    case submitTest
    /// Refreshing authentication token
    case refreshToken
    /// Fetching user profile
    case fetchProfile
    /// Updating user profile
    case updateProfile
    /// Fetching test history
    case fetchHistory
    /// User logout operation
    case logout
    /// Generic network operation
    case generic

    /// User-friendly name for the operation
    var userFacingName: String {
        switch self {
        case .login:
            "signing in"
        case .register:
            "creating account"
        case .fetchQuestions:
            "loading questions"
        case .submitTest:
            "submitting test"
        case .refreshToken:
            "refreshing session"
        case .fetchProfile:
            "loading profile"
        case .updateProfile:
            "updating profile"
        case .fetchHistory:
            "loading history"
        case .logout:
            "signing out"
        case .generic:
            "completing request"
        }
    }
}

enum APIError: Error, LocalizedError {
    case invalidURL
    case invalidResponse
    case unauthorized
    case forbidden
    case notFound
    case serverError(statusCode: Int)
    case decodingError(Error)
    case networkError(Error)
    case unknown

    var errorDescription: String? {
        switch self {
        case .invalidURL:
            "Invalid URL"
        case .invalidResponse:
            "Invalid response from server"
        case .unauthorized:
            "Unauthorized. Please log in again."
        case .forbidden:
            "Access forbidden"
        case .notFound:
            "Resource not found"
        case let .serverError(statusCode):
            "Server error (code: \(statusCode))"
        case let .decodingError(error):
            "Failed to decode response: \(error.localizedDescription)"
        case let .networkError(error):
            "Network error: \(error.localizedDescription)"
        case .unknown:
            "An unknown error occurred"
        }
    }
}

struct ErrorResponse: Codable {
    let detail: String
}
