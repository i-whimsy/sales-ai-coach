@echo off
chcp 65001 >nul
echo ===============================================
echo 🚀 AI Sales Coaching Frontend
echo ===============================================
echo.

:: Navigate to frontend directory
cd frontend

:: Check Node.js
echo Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js not found
    pause
    exit /b 1
)
echo ✅ Node.js found

:: Check npm
echo Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo ❌ npm not found
    pause
    exit /b 1
)
echo ✅ npm found

:: Install dependencies
if not exist "node_modules" (
    echo.
    echo 📦 Installing frontend dependencies...
    npm install
    echo ✅ Dependencies installed
)

:: Start the server
echo.
echo 🎯 Starting frontend server...
echo 📋 Access address: http://localhost:3000
echo.
echo ⏹️  Press Ctrl+C to stop the server
echo ===============================================
echo.

:: Run the server
npm run dev