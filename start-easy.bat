@echo off
chcp 65001 >nul
echo ===============================================
echo 🚀 Starting AI Sales Coaching System
echo ===============================================
echo.

:: Check Python
echo Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    pause
    exit /b 1
)
echo ✅ Python found

:: Check Node.js
echo.
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found
    pause
    exit /b 1
)
echo ✅ Node.js found

:: Create logs folder
if not exist "logs" mkdir logs

:: Start backend
echo.
echo 🎯 Starting backend server...

:: Check virtual environment
if not exist "backend\venv" (
    echo 🔧 Creating virtual environment...
    python -m venv backend\venv
    call backend\venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    echo ✅ Virtual environment created
)

:: Start backend server
start "AI Sales Backend" python backend\main.py
echo ✅ Backend server started on port 8000

:: Wait for backend
ping -n 3 127.0.0.1 >nul

:: Check backend health
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 0 (
    echo ✅ Backend health check passed
) else (
    echo ⚠️  Backend might not be fully ready yet
)

:: Start frontend
echo.
echo 🎯 Starting frontend server...

:: Check frontend dependencies
if not exist "frontend-vue\node_modules" (
    echo 🔧 Installing frontend dependencies...
    cd frontend-vue
    npm install
    cd ..
    echo ✅ Frontend dependencies installed
)

:: Start frontend server
start "AI Sales Frontend" /D "frontend-vue" npm run dev
echo ✅ Frontend server started on port 3002

:: Wait for frontend
ping -n 5 127.0.0.1 >nul

:: Open browser
echo.
echo 🌐 Opening browser...
start http://localhost:3002

echo.
echo ===============================================
echo 🎉 System started successfully!
echo ===============================================
echo.
echo 📊 Access addresses:
echo    Frontend: http://localhost:3002
echo    Backend:  http://localhost:8000
echo.
echo 📋 Log files are in the logs folder
echo ===============================================
echo.
echo Press any key to exit...
pause >nul