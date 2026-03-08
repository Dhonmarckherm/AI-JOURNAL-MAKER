@echo off
echo ========================================
echo   AI Journal Maker - Railway Deploy
echo ========================================
echo.

REM Check if logged in
echo [INFO] Checking Railway login status...
railway whoami >nul 2>&1
if errorlevel 1 (
    echo [ACTION] Please login to Railway first
    echo.
    echo Run: railway login
    echo.
    pause
    exit /b 1
)

echo [INFO] Logged in successfully
echo.

REM Initialize project if needed
if not exist ".railway" (
    echo [INFO] Initializing Railway project...
    railway init
    if errorlevel 1 (
        echo [ERROR] Failed to initialize Railway project
        pause
        exit /b 1
    )
)

echo.
echo [INFO] Adding PostgreSQL database...
railway add postgres --yes 2>nul
if errorlevel 1 (
    echo [WARN] Database might already exist, continuing...
)

echo.
echo [INFO] Setting environment variables...
railway variables set OPENROUTER_API_KEY=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

echo.
echo [INFO] Deploying to Railway...
railway up

echo.
echo ========================================
echo   Deployment Complete!
echo ========================================
echo.
echo To get your app URL, run:
echo   railway domain
echo.
echo To view logs, run:
echo   railway logs
echo.
pause
