@echo off
chcp 65001 >nul
echo ===============================================
echo 🚀 AI Sales Coaching Backend v2.0.0
echo ===============================================
echo.

:: Navigate to backend directory
cd backend

:: Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    pause
    exit /b 1
)
echo ✅ Python found

:: Setup virtual environment
if not exist "venv" (
    echo.
    echo 🔧 Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
)

:: Activate virtual environment and install dependencies
echo.
echo 📦 Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt
echo ✅ Dependencies installed

:: Start the server
echo.
echo 🎯 Starting backend server...
echo 📋 Access addresses:
echo    - API: http://localhost:8000
echo    - Docs: http://localhost:8000/docs
echo    - Health: http://localhost:8000/health
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo ===============================================
echo.

:: Run the server
python new_app.py