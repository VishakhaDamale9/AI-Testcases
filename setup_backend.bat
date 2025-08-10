@echo off
echo Setting up backend virtual environment and installing dependencies...

:: Create virtual environment
python -m venv backend\venv

:: Activate virtual environment
call backend\venv\Scripts\activate.bat

:: Install dependencies with exact versions
pip install -r backend\requirements.txt

:: Run initial setup
cd backend
python -m app.backend_pre_start
python -m app.initial_data

echo Backend setup complete!