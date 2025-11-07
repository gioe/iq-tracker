import Foundation

struct TestResult: Codable, Identifiable {
    let id: String
    let testSessionId: String
    let userId: String
    let iqScore: Int
    let totalQuestions: Int
    let correctAnswers: Int
    let completionTimeSeconds: Int
    let completedAt: Date

    var accuracy: Double {
        guard totalQuestions > 0 else { return 0 }
        return Double(correctAnswers) / Double(totalQuestions)
    }

    var completionTimeFormatted: String {
        let minutes = completionTimeSeconds / 60
        let seconds = completionTimeSeconds % 60
        return String(format: "%d:%02d", minutes, seconds)
    }

    enum CodingKeys: String, CodingKey {
        case id
        case testSessionId = "test_session_id"
        case userId = "user_id"
        case iqScore = "iq_score"
        case totalQuestions = "total_questions"
        case correctAnswers = "correct_answers"
        case completionTimeSeconds = "completion_time_seconds"
        case completedAt = "completed_at"
    }
}
