@echo off
REM This script installs dependencies and runs the app
cd /d "%~dp0"

echo.
echo ====================================================================
echo              Multi-Agent Game Tester POC - Demo Start
echo ====================================================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found!
    echo Please install Python from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)

echo [1/4] Setting up virtual environment...
if not exist venv (
    python -m venv venv
)

call venv\Scripts\activate.bat

echo [2/4] Installing dependencies... (this may take 2-3 minutes)
pip install fastapi uvicorn playwright langchain langchain-community pydantic python-dotenv aiofiles requests pillow >nul 2>&1

echo [3/4] Creating necessary folders...
if not exist reports mkdir reports
if not exist artifacts mkdir artifacts

echo [4/4] Starting server...
echo.
echo ====================================================================
echo                    SERVER STARTING...
echo ====================================================================
echo.
echo Web Interface: http://localhost:8000/app
echo API Server   : http://localhost:8000
echo.
echo The browser should open automatically...
echo If not, open http://localhost:8000 in your browser
echo.
echo Press Ctrl+C to stop the server
echo ====================================================================
echo.


START http://localhost:8000/app

uvicorn api.index:app --host 0.0.0.0 --port 8000

pause
