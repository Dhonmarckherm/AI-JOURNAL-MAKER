@echo off
echo ========================================
echo   AI Journal Maker - Startup Script
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [INFO] Creating .env file from .env.example...
    copy ".env.example" ".env"
    echo [ACTION] Please edit .env file and add your API key
    echo.
    pause
    exit /b 1
)

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
echo [INFO] Checking dependencies...
pip install -r requirements_journal.txt -q

REM Start the application
echo.
echo [INFO] Starting AI Journal Maker...
echo [INFO] Open http://localhost:8000 in your browser
echo.
python journal_app.py

pause
