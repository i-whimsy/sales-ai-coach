# AI Sales Coaching System Startup Script
# Pure English Version

Clear-Host
Write-Host "==============================================="
Write-Host "🚀 AI Sales Coaching System" -ForegroundColor Cyan
Write-Host "==============================================="
Write-Host ""

# Check Python
Write-Host "🔍 Checking for Python..."
if (Get-Command python -ErrorAction SilentlyContinue) {
    Write-Host "✅ Python is installed" -ForegroundColor Green
} else {
    Write-Host "❌ Python is not installed" -ForegroundColor Red
    Write-Host "Please install Python from https://www.python.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Check Node.js
Write-Host ""
Write-Host "🔍 Checking for Node.js..."
if (Get-Command node -ErrorAction SilentlyContinue) {
    Write-Host "✅ Node.js is installed" -ForegroundColor Green
} else {
    Write-Host "❌ Node.js is not installed" -ForegroundColor Red
    Write-Host "Please install Node.js from https://nodejs.org/"
    Read-Host "Press Enter to exit"
    exit 1
}

# Create logs directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Start backend server
Write-Host ""
Write-Host "🎯 Starting Backend Server..." -ForegroundColor Yellow

# Setup virtual environment
if (-not (Test-Path "backend\venv")) {
    Write-Host "🔧 Creating virtual environment..." -ForegroundColor Cyan
    python -m venv backend\venv
    & backend\venv\Scripts\Activate.ps1
    pip install -r backend\requirements.txt
    Write-Host "✅ Virtual environment setup complete" -ForegroundColor Green
}

# Start backend
Start-Process -FilePath "python" -ArgumentList "backend\main.py" -WindowStyle Normal -WorkingDirectory $PWD.Path
Write-Host "✅ Backend server started on port 8000" -ForegroundColor Green

# Wait for backend initialization
Write-Host """⏳ Waiting for backend to initialize..."
Start-Sleep -Seconds 3

# Check backend health
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ Backend health check passed" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Backend is still starting up, please check status later" -ForegroundColor Yellow
}

# Start frontend server
Write-Host ""
Write-Host "🎯 Starting Frontend Server..." -ForegroundColor Yellow

# Install frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "🔧 Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✅ Frontend dependencies installed" -ForegroundColor Green
}

# Start frontend
Push-Location frontend
Start-Process -FilePath "npm.cmd" -ArgumentList "run dev" -WindowStyle Normal -WorkingDirectory $PWD.Path
Pop-Location
Write-Host "✅ Frontend server started on port 3000" -ForegroundColor Green

# Wait for frontend initialization
Write-Host """⏳ Waiting for frontend to initialize..."
Start-Sleep -Seconds 5

# Open browser
Write-Host ""
Write-Host "🌐 Opening browser..." -ForegroundColor Yellow
try {
    Start-Process "http://localhost:3000"
    Write-Host "✅ Browser opened to frontend interface" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Failed to open browser, please manually visit http://localhost:3000" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "==============================================="
Write-Host "🎉 System Startup Complete!" -ForegroundColor Green
Write-Host "==============================================="
Write-Host ""
Write-Host "📊 Access Information:"
Write-Host "   Frontend UI: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "📋 Logging:" -ForegroundColor White
Write-Host "   Log files are stored in the 'logs' directory"
Write-Host ""
Write-Host "⏹️ To stop the system, close all console windows"
Write-Host ""
Read-Host "Press Enter to close this window"