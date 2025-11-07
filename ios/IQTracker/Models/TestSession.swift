import Foundation

enum TestStatus: String, Codable {
    case inProgress = "in_progress"
    case completed
    case abandoned
}

struct TestSession: Codable, Identifiable {
    let id: String
    let userId: String
    let startedAt: Date
    let completedAt: Date?
    let status: TestStatus
    let questions: [Question]

    enum CodingKeys: String, CodingKey {
        case id
        case userId = "user_id"
        case startedAt = "started_at"
        case completedAt = "completed_at"
        case status
        case questions
    }
}

struct TestSubmission: Codable {
    let testSessionId: String
    let responses: [QuestionResponse]

    enum CodingKeys: String, CodingKey {
        case testSessionId = "test_session_id"
        case responses
    }
}
