# IQ Tracker iOS App

Native iOS application for tracking IQ scores over time.

## Features

- Gamified IQ test interface
- Historical score tracking
- Trend visualization and insights
- Push notifications for periodic test reminders
- Secure user authentication

## Tech Stack

- SwiftUI
- iOS 15+ (target to be determined)
- Swift Package Manager for dependencies

## Setup

### Prerequisites

- Xcode 14+ installed
- macOS with Apple Silicon or Intel processor
- Apple Developer account (for deployment)
- **SwiftLint** - Code linting tool
- **SwiftFormat** - Code formatting tool

### Install Code Quality Tools

```bash
# Install via Homebrew
brew install swiftlint swiftformat
```

### Getting Started

1. Open the Xcode project:
   ```bash
   open IQTracker.xcodeproj
   # or
   open IQTracker.xcworkspace
   ```

2. Select your development team in project settings

3. Build and run on simulator or device

## Project Structure

(To be added once Xcode project is created)

## Code Quality

This project uses SwiftLint and SwiftFormat to maintain code quality and consistency.

### Configuration Files

- **`.swiftlint.yml`** - SwiftLint rules and configuration
- **`.swiftformat`** - SwiftFormat rules and configuration
- **`.pre-commit-config.yaml`** - Git hooks configuration (optional)

### Running Manually

**SwiftLint:**
```bash
cd ios
swiftlint lint --config .swiftlint.yml
```

**SwiftFormat:**
```bash
cd ios
# Check formatting
swiftformat --config .swiftformat --lint IQTracker/

# Auto-format files
swiftformat --config .swiftformat IQTracker/
```

### Xcode Integration (Recommended)

SwiftLint and SwiftFormat can be integrated as Xcode build phases to run automatically on every build:

**To add SwiftLint build phase:**
1. In Xcode, select the project in the navigator
2. Select the app target
3. Go to "Build Phases" tab
4. Click "+" and select "New Run Script Phase"
5. Add: `swiftlint lint --config ${SRCROOT}/.swiftlint.yml`
6. Move this phase before "Compile Sources"

**To add SwiftFormat build phase (optional):**
1. Follow same steps as SwiftLint
2. Add: `swiftformat --config ${SRCROOT}/.swiftformat ${SRCROOT}/IQTracker/`

### Pre-Commit Hooks (Optional)

For developers who prefer git hooks:

```bash
# From the repository root
pip install pre-commit
cd ios
pre-commit install
```

Now SwiftLint and SwiftFormat will run automatically before each commit.

## Configuration

(To be added)

## Building for App Store

(To be added)
