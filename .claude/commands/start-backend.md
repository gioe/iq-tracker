# Start Backend

Start the FastAPI backend server in the background. Kill any existing processes on port 8000 first.

Run this command:
```bash
lsof -ti :8000 | xargs kill -9 2>/dev/null; sleep 1 && cd /Users/mattgioe/aiq/backend && source venv/bin/activate && uvicorn app.main:app --reload
```

Run this in the background and check the output to confirm it started successfully. The API docs will be available at http://localhost:8000/v1/docs
