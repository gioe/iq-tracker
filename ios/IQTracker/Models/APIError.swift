import Foundation

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
