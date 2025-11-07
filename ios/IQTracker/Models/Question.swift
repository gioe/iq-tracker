import Foundation

enum QuestionType: String, Codable {
    case pattern = "pattern"
    case logic = "logic"
    case spatial = "spatial"
    case math = "math"
    case verbal = "verbal"
    case memory = "memory"
}

enum DifficultyLevel: String, Codable {
    case easy = "easy"
    case medium = "medium"
    case hard = "hard"
}

struct Question: Codable, Identifiable {
    let id: String
    let questionText: String
    let questionType: QuestionType
    let difficultyLevel: DifficultyLevel
    let answerOptions: [String]?
    let explanation: String?

    enum CodingKeys: String, CodingKey {
        case id
        case questionText = "question_text"
        case questionType = "question_type"
        case difficultyLevel = "difficulty_level"
        case answerOptions = "answer_options"
        case explanation
    }
}

struct QuestionResponse: Codable {
    let questionId: String
    let userAnswer: String

    enum CodingKeys: String, CodingKey {
        case questionId = "question_id"
        case userAnswer = "user_answer"
    }
}
