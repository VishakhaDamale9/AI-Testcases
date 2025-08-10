@echo off
echo Setting up and running the full-stack application...

:: Setup backend
call setup_backend.bat

:: Setup frontend
call setup_frontend.bat

:: Run backend tests
call run_backend_tests.bat

:: Run frontend tests
call run_frontend_tests.bat

:: Run the application
call run_app.bat

echo Setup and running complete!