# IQ Tracker

An iOS application that tracks users' IQ scores over time through periodic testing with AI-generated questions.

## Project Structure

This is a monorepo containing all components of the IQ Tracker application:

```
iq-tracker/
├── ios/                    # SwiftUI iOS application
├── backend/                # Backend API server
├── question-service/       # AI-powered question generation service
├── shared/                 # Shared schemas, types, and documentation
├── .github/workflows/      # CI/CD pipelines
└── README.md              # This file
```

## Components

### iOS App (`ios/`)
- Native iOS application built with SwiftUI
- Gamified IQ test experience
- Historical score tracking and trend visualization
- Push notification support for periodic test reminders

### Backend (`backend/`)
- REST API server
- User authentication and management
- Question serving and response storage
- Results calculation and analytics
- Push notification scheduling

### Question Service (`question-service/`)
- Autonomous service for generating novel IQ test questions
- Multi-LLM architecture with quality arbiter
- Ensures continuous supply of fresh questions
- Prevents question repetition per user

## Getting Started

See individual component READMEs for setup instructions:
- [iOS App Setup](ios/README.md)
- [Backend Setup](backend/README.md)
- [Question Service Setup](question-service/README.md)

## Development

(Development guidelines to be added)

## Deployment

(Deployment instructions to be added)
