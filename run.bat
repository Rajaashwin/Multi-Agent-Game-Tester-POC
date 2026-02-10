@echo off
echo.
echo ======================================
echo Multi-Agent Game Tester POC
echo ======================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.9+ from https://www.python.org/
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install requirements
echo Installing dependencies...
pip install -r requirements.txt

REM Create necessary directories
if not exist "reports" mkdir reports
if not exist "artifacts" mkdir artifacts

REM Start the application
echo.
echo ======================================
echo Starting FastAPI Server...
echo ======================================
echo.
echo Server will start at http://localhost:8000
echo Frontend: http://localhost:8000/app
echo.
echo Press Ctrl+C to stop the server
echo.

uvicorn api.index:app --host 0.0.0.0 --port 8000

pause
