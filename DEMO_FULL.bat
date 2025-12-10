@echo off
setlocal enabledelayedexpansion

REM ===================================================
REM BDD Demo Workflow Script
REM ===================================================
REM 1) Creates/uses backend venv
REM 2) Runs baseline pytest with coverage.xml
REM 3) Prints coverage gaps
REM 4) Generates BDD tests with Groq (coverage-aware)
REM 5) Runs behave + final coverage (html)
REM ===================================================
echo ===================================================
echo BDD Test Generation and 100%% Coverage Achievement
echo ===================================================

REM Establish key paths
set ROOT=%~dp0
set BACKEND=%ROOT%backend
set PYTHON_EXE=%BACKEND%\venv\Scripts\python.exe

pushd "%ROOT%"

REM Create backend virtual environment if missing
if not exist "%BACKEND%\venv" (
    echo Creating backend virtual environment...
    pushd "%BACKEND%"
    python -m venv venv
    popd
)

REM Activate the virtual environment
call "%BACKEND%\venv\Scripts\activate"

REM Install required packages (idempotent)
echo Ensuring dependencies are installed...
"%PYTHON_EXE%" -m pip install --quiet --upgrade pip
"%PYTHON_EXE%" -m pip install --quiet pytest pytest-cov behave fastapi httpx alembic -r "%BACKEND%\requirements.txt"

REM Run database migrations before tests
echo.
echo ===================================================
echo Running database migrations...
echo ===================================================
pushd "%BACKEND%"
"%PYTHON_EXE%" -m alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed. Please check your database connection and .env file.
    popd
    popd
    pause
    exit /b 1
)
popd

REM Create necessary directories
if not exist "%BACKEND%\app\tests\features\steps" (
    mkdir "%BACKEND%\app\tests\features\steps"
)

REM Run initial tests to get baseline coverage (produces coverage.xml)
echo.
echo ===================================================
echo Running initial tests to get baseline coverage...
echo ===================================================
pushd "%BACKEND%"
"%PYTHON_EXE%" -m pytest --cov=app --cov-report=term --cov-report=xml
popd

REM Analyze coverage gaps
echo.
echo ===================================================
echo Analyzing coverage gaps...
echo ===================================================
"%PYTHON_EXE%" "%ROOT%analyze_coverage_gaps.py" --coverage-xml "%BACKEND%\coverage.xml"

REM Clear old generated tests for a fresh start
echo.
echo ===================================================
echo Clearing old generated BDD tests...
echo ===================================================
del /Q "%BACKEND%\app\tests\features\*.feature" 2>nul
del /Q "%BACKEND%\app\tests\features\steps\*_steps.py" 2>nul
echo Old tests cleared.

REM Run Groq BDD generator (coverage-aware)
echo.
echo ===================================================
echo Running Groq BDD generator...
echo ===================================================
"%PYTHON_EXE%" "%ROOT%bdd_test_generator.py" --coverage-xml "%BACKEND%\coverage.xml"

REM Run the generated BDD tests
echo.
echo ===================================================
echo Running generated BDD tests...
echo ===================================================
pushd "%BACKEND%"
"%PYTHON_EXE%" -m behave app\tests\features

REM Final coverage check (HTML report)
echo.
echo ===================================================
echo Final coverage check...
echo ===================================================
"%PYTHON_EXE%" -m pytest --cov=app --cov-report=term --cov-report=html --cov-fail-under=100

REM Open coverage report in browser if available
if exist "%BACKEND%\htmlcov\index.html" (
    echo Opening coverage report in browser...
    start "" "%BACKEND%\htmlcov\index.html"
)
popd

REM Deactivate virtual environment
call deactivate
popd

echo.
echo ===================================================
echo Process complete!
echo ===================================================
echo If 100%% coverage was not achieved, review the coverage report
echo and add more test scenarios to cover the remaining gaps.
echo You can run this script again to continue improving coverage.

pause