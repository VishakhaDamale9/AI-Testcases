@echo off
echo Running backend tests with 100% coverage...

:: Activate virtual environment
call backend\venv\Scripts\activate.bat

:: Navigate to backend directory
cd backend

:: Run pytest with coverage
python -m pytest --cov=app --cov-report=term --cov-report=html --cov-report=xml --cov-fail-under=100

:: Run BDD tests
python -m behave app/tests/features

echo Backend tests complete!