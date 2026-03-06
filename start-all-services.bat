@echo off
chcp 65001 >nul
echo ===============================================
echo 🚀 AI Sales Coaching System v2.0.0
echo ===============================================
echo.

:: Check prerequisites
echo 🔍 Checking system prerequisites...

:: Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found
    pause
    exit /b 1
)
echo ✅ Python found

:: Check Node.js
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found
    pause
    exit /b 1
)
echo ✅ Node.js found

:: Check npm
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm not found
    pause
    exit /b 1
)
echo ✅ npm found

echo.
echo ✅ All prerequisites met

:: Create logs directory
if not exist "logs" mkdir logs

:: Start backend server
echo.
echo 🎯 Starting backend server...
start "Backend Server" /MIN start-backend.bat
echo ✅ Backend server started in separate window

:: Wait for backend to initialize
echo.
echo ⏳ Waiting for backend to initialize...
ping -n 5 127.0.0.1 >nul

:: Start frontend server
echo.
echo 🎯 Starting frontend server...
start "Frontend Server" /MIN start-frontend.bat
echo ✅ Frontend server started in separate window

:: Wait for servers to start
echo.
echo ⏳ Waiting for servers to fully start...
ping -n 10 127.0.0.1 >nul

:: Check services
echo.
echo 🩺 Checking service health...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 0 (
    echo ✅ Backend service is healthy
) else (
    echo ⚠️  Backend may still be starting up
)

:: Open browser
echo.
echo 🌐 Opening browser...
start http://localhost:3000

echo.
echo ===============================================
echo 🎉 System startup complete!
echo ===============================================
echo.
echo 📊 Access addresses:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:8000
echo    API Docs: http://localhost:8000/docs
echo.
echo 📋 Logs will be shown in separate windows
echo ⏹️  To stop, close all command windows
echo ===============================================
echo.
pause