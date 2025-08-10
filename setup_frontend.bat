@echo off
echo Setting up frontend dependencies...

:: Navigate to frontend directory
cd frontend

:: Install dependencies with exact versions
npm ci

:: Generate API client
npm run generate-client

echo Frontend setup complete!