[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# AI Sales Coach System One-Click Startup Script
# PowerShell Version

Write-Host "Starting AI Sales Coach System..." -ForegroundColor Cyan

# Check if Python is available
try {
    $null = python --version
    Write-Host "Python environment detected" -ForegroundColor Green
} catch {
    Write-Host "Python not found, please install Python first" -ForegroundColor Red
    exit 1
}

# Check if Node.js is available
try {
    $null = node --version
    Write-Host "Node.js environment detected" -ForegroundColor Green
} catch {
    Write-Host "Node.js not found, please install Node.js first" -ForegroundColor Red
    exit 1
}

# Create output directory
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# Start backend service
Write-Host "`nStarting backend server..." -ForegroundColor Yellow

# Check backend dependencies
if (-not (Test-Path "backend\venv")) {
    Write-Host "Creating and configuring virtual environment..." -ForegroundColor Cyan
    python -m venv backend\venv
    & backend\venv\Scripts\Activate.ps1
    pip install -r backend\requirements.txt
    Write-Host "Virtual environment configuration completed" -ForegroundColor Green
}

# Start backend
$backendProcess = Start-Process -FilePath "backend\venv\Scripts\python.exe" -ArgumentList "backend\main.py" -WorkingDirectory $PWD.Path -RedirectStandardOutput "logs\backend.log" -RedirectStandardError "logs\backend_error.log" -PassThru
Write-Host "Backend server started (Port: 8000, PID: $($backendProcess.Id))" -ForegroundColor Green

# Wait for backend to start
Start-Sleep -Seconds 3

# Check if backend started successfully
try {
    $null = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "Backend service health check passed" -ForegroundColor Green
} catch {
    Write-Host "Backend service may not have started completely, please check later" -ForegroundColor Yellow
}

# Start frontend service
Write-Host "`nStarting frontend server..." -ForegroundColor Yellow

# Check frontend dependencies
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "Installing frontend dependencies..." -ForegroundColor Cyan
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "Frontend dependencies installation completed" -ForegroundColor Green
}

# Start frontend
$frontendProcess = Start-Process -FilePath "cmd" -ArgumentList "/c npm run dev" -WorkingDirectory (Join-Path $PWD.Path "frontend") -RedirectStandardOutput "logs\frontend.log" -RedirectStandardError "logs\frontend_error.log" -PassThru -WindowStyle Hidden
Write-Host "Frontend server started (Port: 3000, PID: $($frontendProcess.Id))" -ForegroundColor Green

# Wait for frontend to start
Start-Sleep -Seconds 5

# Start browser
Write-Host "`nStarting browser..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host "`nAI Sales Coach System startup completed!" -ForegroundColor Green
Write-Host "System access addresses:" -ForegroundColor Cyan
Write-Host "   Frontend interface: http://localhost:3000" -ForegroundColor White
Write-Host "   Backend API:       http://localhost:8000" -ForegroundColor White
Write-Host "`nLog file locations:" -ForegroundColor Cyan
Write-Host "   Frontend log: logs/frontend.log" -ForegroundColor White
Write-Host "   Backend log:  logs/backend.log" -ForegroundColor White
Write-Host "`nTo stop services, close all command windows or press Ctrl+C" -ForegroundColor Yellow