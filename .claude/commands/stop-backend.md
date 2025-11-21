# Stop Backend

Stop the FastAPI backend server by killing any processes on port 8000.

Run this command:
```bash
lsof -ti :8000 | xargs kill -9 2>/dev/null && echo "Backend server stopped" || echo "No backend server running on port 8000"
```
