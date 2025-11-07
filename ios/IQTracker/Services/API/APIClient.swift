import Foundation

/// Protocol defining the API client interface
protocol APIClientProtocol {
    func request<T: Decodable>(
        endpoint: APIEndpoint,
        method: HTTPMethod,
        body: Encodable?,
        requiresAuth: Bool
    ) async throws -> T
}

/// HTTP methods supported by the API
enum HTTPMethod: String {
    case get = "GET"
    case post = "POST"
    case put = "PUT"
    case delete = "DELETE"
}

/// API endpoint definitions
enum APIEndpoint {
    case register
    case login
    case refreshToken
    case logout
    case userProfile
    case testStart
    case testSubmit
    case testResults(String)
    case testHistory

    var path: String {
        switch self {
        case .register:
            return "/v1/auth/register"
        case .login:
            return "/v1/auth/login"
        case .refreshToken:
            return "/v1/auth/refresh"
        case .logout:
            return "/v1/auth/logout"
        case .userProfile:
            return "/v1/user/profile"
        case .testStart:
            return "/v1/test/start"
        case .testSubmit:
            return "/v1/test/submit"
        case .testResults(let testId):
            return "/v1/test/results/\(testId)"
        case .testHistory:
            return "/v1/test/history"
        }
    }
}

/// Main API client implementation
class APIClient: APIClientProtocol {
    private let baseURL: URL
    private let session: URLSession
    private var authToken: String?

    init(baseURL: String, session: URLSession = .shared) {
        guard let url = URL(string: baseURL) else {
            fatalError("Invalid base URL: \(baseURL)")
        }
        self.baseURL = url
        self.session = session
    }

    func setAuthToken(_ token: String?) {
        self.authToken = token
    }

    func request<T: Decodable>(
        endpoint: APIEndpoint,
        method: HTTPMethod = .get,
        body: Encodable? = nil,
        requiresAuth: Bool = true
    ) async throws -> T {
        guard let url = URL(string: endpoint.path, relativeTo: baseURL) else {
            throw APIError.invalidURL
        }

        var request = URLRequest(url: url)
        request.httpMethod = method.rawValue
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        // Add auth token if required
        if requiresAuth, let token = authToken {
            request.setValue("Bearer \(token)", forHTTPHeaderField: "Authorization")
        }

        // Encode body if present
        if let body = body {
            request.httpBody = try JSONEncoder().encode(body)
        }

        // Perform request
        let (data, response) = try await session.data(for: request)

        // Check response status
        guard let httpResponse = response as? HTTPURLResponse else {
            throw APIError.invalidResponse
        }

        switch httpResponse.statusCode {
        case 200...299:
            // Success - decode response
            do {
                let decoder = JSONDecoder()
                decoder.dateDecodingStrategy = .iso8601
                return try decoder.decode(T.self, from: data)
            } catch {
                throw APIError.decodingError(error)
            }
        case 401:
            throw APIError.unauthorized
        case 403:
            throw APIError.forbidden
        case 404:
            throw APIError.notFound
        case 500...599:
            throw APIError.serverError(statusCode: httpResponse.statusCode)
        default:
            throw APIError.unknown
        }
    }
}
