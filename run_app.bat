@echo off
setlocal enabledelayedexpansion

echo Starting the full-stack application...

REM Check if venv exists
if not exist "backend\venv" (
    echo ERROR: Virtual environment not found. Please run DEMO_FULL.bat first or create venv manually.
    pause
    exit /b 1
)

REM Run database migrations before starting
echo.
echo Running database migrations...
cd backend
call venv\Scripts\activate
python -m alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed. Please check your database connection and .env file.
    pause
    exit /b 1
)
cd ..

echo.
echo Starting servers...

:: Start backend in a new window (limit reload watch to app/ to avoid venv issues)
start cmd /k "cd backend && .\venv\Scripts\activate && python -m uvicorn app.main:app --reload --reload-dir app --port 8000"

:: Start frontend in a new window
start cmd /k "cd frontend && npm run dev"

echo.
echo Application started!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:5173
echo.
echo Note: If you see database errors, ensure PostgreSQL is running and migrations completed.
pause