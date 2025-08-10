@echo off
echo ===================================================
echo BDD Test Generation and 100%% Coverage Achievement
echo ===================================================

REM Set working directory
cd %~dp0

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

REM Run initial tests to get baseline coverage
echo \n===================================================
echo Running initial tests to get baseline coverage...
echo ===================================================
python -m pytest --cov=app --cov-report=term --cov-report=xml

REM Return to root directory
cd ..

REM Analyze coverage gaps
echo \n===================================================
echo Analyzing coverage gaps...
echo ===================================================
python analyze_coverage_gaps.py

REM Run Groq BDD generator
echo \n===================================================
echo Running Groq BDD generator...
echo ===================================================
python groq_bdd_generator.py

REM Run the generated BDD tests
echo \n===================================================
echo Running generated BDD tests...
echo ===================================================
cd backend
python -m behave app\tests\features

REM Run CI/CD integration script with target coverage 100%
echo \n===================================================
echo Running CI/CD integration for iterative improvement...
echo ===================================================
cd ..
python ci_cd_integration.py --target-coverage 100 --max-iterations 3

REM Final coverage check
echo \n===================================================
echo Final coverage check...
echo ===================================================
cd backend
python -m pytest --cov=app --cov-report=term --cov-report=html --cov-fail-under=100

REM Open coverage report in browser if available
if exist htmlcov\index.html (
    echo Opening coverage report in browser...
    start htmlcov\index.html
)

REM Deactivate virtual environment
call deactivate
cd ..

echo \n===================================================
echo Process complete!
echo ===================================================
echo If 100%% coverage was not achieved, review the coverage report
echo and add more test scenarios to cover the remaining gaps.
echo \nYou can run this script again to continue improving coverage.

pause