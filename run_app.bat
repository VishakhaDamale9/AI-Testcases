@echo off
echo Starting the full-stack application...

:: Start backend in a new window
start cmd /k "cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload --port 8000"

:: Start frontend in a new window
start cmd /k "cd frontend && npm run dev"

echo Application started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173