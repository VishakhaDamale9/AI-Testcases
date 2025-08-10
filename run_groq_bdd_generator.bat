@echo off
echo Starting Groq BDD Test Generator...

REM Check if backend virtual environment exists
if not exist backend\venv (
    echo Creating backend virtual environment...
    cd backend
    python -m venv venv
    call venv\Scripts\activate
    pip install -r requirements.txt
    cd ..
) else (
    echo Backend virtual environment already exists.
)

REM Activate the virtual environment
cd backend
call venv\Scripts\activate

REM Install required packages if not already installed
pip install pytest pytest-cov behave fastapi httpx

REM Create necessary directories
if not exist app\tests\features\steps (
    mkdir app\tests\features\steps
)

REM Return to root directory
cd ..

REM Run the Groq BDD generator
echo Running Groq BDD generator...
python groq_bdd_generator.py

REM Run the generated BDD tests
echo Running generated BDD tests...
cd backend
python -m behave app\tests\features

REM Run pytest with coverage
echo Running pytest with coverage...
python -m pytest --cov=app --cov-report=term --cov-report=xml --cov-fail-under=100

REM Deactivate virtual environment
call deactivate
cd ..

echo BDD test generation and execution complete!
pause