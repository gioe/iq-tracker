# Test All

Run tests for all components (backend and iOS).

Run these commands sequentially:

1. Backend tests:
```bash
cd /Users/mattgioe/aiq/backend && source venv/bin/activate && pytest
```

2. iOS tests:
```bash
cd /Users/mattgioe/aiq/ios && xcodebuild test -scheme AIQ -destination 'platform=iOS Simulator,name=iPhone 15' -quiet
```

Report results for each component, noting any failures.
