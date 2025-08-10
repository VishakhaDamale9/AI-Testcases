@echo off
echo Generating BDD tests and running coverage analysis...

:: Activate virtual environment
IF NOT EXIST backend\venv (
    echo Creating virtual environment...
    cd backend
    python -m venv venv
    cd ..
)
call backend\venv\Scripts\activate.bat

:: Install required packages if needed
pip install pytest pytest-cov behave fastapi httpx

:: Run initial tests to get baseline coverage
echo Running initial tests to get baseline coverage...
cd backend
python -m pytest --cov=app --cov-report=term --cov-report=xml
cd ..

:: Run the enhanced prompt engineering BDD test generation script
echo Running prompt engineering BDD test generation script...
python prompt_engineering_bdd.py --target-coverage=100.0 --max-iterations=3

:: Run the final tests with coverage check
echo Running final tests with coverage check...
cd backend
python -m behave app/tests/features
python -m pytest --cov=app --cov-report=term --cov-report=html --cov-fail-under=100
cd ..

echo BDD test generation and coverage analysis complete!
pause