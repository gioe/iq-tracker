# IQ Tracker Question Generation Service

Autonomous service for generating novel IQ test questions using AI.

## Purpose

Continuously generates fresh, high-quality IQ test questions to prevent users from encountering repeated questions and to ensure test validity over time.

## Architecture

### Multi-LLM Design

This service employs multiple Large Language Models to generate diverse questions:

1. **Generator LLMs** - Multiple models create candidate questions
   - Diversity in question types and difficulty
   - Different models bring different strengths

2. **Arbiter LLM** - Quality control layer
   - Evaluates generated questions for:
     - Clarity and unambiguity
     - Appropriate difficulty level
     - Validity as an IQ test question
     - Novelty (not duplicating existing questions)
   - Approves or rejects candidate questions

## Question Types

(To be defined - typical IQ test categories include:)
- Pattern recognition
- Logical reasoning
- Spatial reasoning
- Mathematical problems
- Verbal reasoning
- Memory-based questions

## Tech Stack

(To be determined)

## Process Flow

1. Service runs on a schedule (e.g., daily/weekly)
2. Generator LLMs create batches of candidate questions
3. Arbiter LLM evaluates each candidate
4. Approved questions are inserted into database
5. Questions are tagged with metadata (type, difficulty, etc.)
6. System ensures no duplicates exist

## Setup

(To be added once tech stack is chosen)

## Configuration

(To be added)

## Monitoring

(To be added - should track:)
- Questions generated per run
- Approval/rejection rates
- Question pool size
- Coverage across question types and difficulties
