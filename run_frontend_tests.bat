@echo off
echo Running frontend tests...

:: Navigate to frontend directory
cd frontend

:: Run Playwright tests
npx playwright test

echo Frontend tests complete!