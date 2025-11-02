# IQ Tracker Backend

Backend API server for the IQ Tracker application.

## Responsibilities

- User authentication and account management
- Serving IQ test questions to iOS app
- Storing user responses and test results
- Calculating scores and generating insights/trends
- Managing push notification scheduling
- Tracking which questions each user has answered

## Tech Stack

(To be determined - options include Node.js, Python/FastAPI, Go, etc.)

## API Endpoints

(To be designed)

### Planned Endpoints:
- Authentication (login, register, token refresh)
- User profile management
- Question fetching (with logic to exclude already-answered questions)
- Response submission
- Results and insights retrieval
- Notification preferences

## Database Schema

(To be designed)

### Planned Tables:
- `users` - User accounts and profiles
- `questions` - IQ test questions pool
- `user_questions` - Tracks which questions each user has seen
- `responses` - User answers to questions
- `test_results` - Aggregated test scores over time
- `notifications` - Notification scheduling and history

## Setup

(To be added once tech stack is chosen)

## Development

(To be added)

## Deployment

(To be added)
