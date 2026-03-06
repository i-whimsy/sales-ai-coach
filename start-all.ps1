# AI销售教练系统一键启动脚本
# PowerShell版本

Write-Host "🚀 启动AI销售教练系统..." -ForegroundColor Cyan

# 检查Python是否可用
try {
    $null = python --version
    Write-Host "✅ Python环境已检测" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Python，请先安装Python" -ForegroundColor Red
    exit 1
}

# 检查Node.js是否可用
try {
    $null = node --version
    Write-Host "✅ Node.js环境已检测" -ForegroundColor Green
} catch {
    Write-Host "❌ 未找到Node.js，请先安装Node.js" -ForegroundColor Red
    exit 1
}

# 创建输出目录
if (-not (Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
}

# 启动后端服务
Write-Host "`n🎯 启动后端服务器..." -ForegroundColor Yellow

# 检查后端依赖
if (-not (Test-Path "backend\venv")) {
    Write-Host "🔧 创建并配置虚拟环境..." -ForegroundColor Cyan
    python -m venv backend\venv
    & backend\venv\Scripts\Activate.ps1
    pip install -r backend\requirements.txt
    Write-Host "✅ 虚拟环境配置完成" -ForegroundColor Green
}

# 启动后端
$backendProcess = Start-Process -FilePath "python" -ArgumentList "backend\main.py" -WorkingDirectory $PWD.Path -RedirectStandardOutput "logs\backend.log" -RedirectStandardError "logs\backend_error.log" -PassThru
Write-Host "✅ 后端服务器已启动 (端口: 8000, PID: $($backendProcess.Id))" -ForegroundColor Green

# 等待后端启动
Start-Sleep -Seconds 3

# 检查后端是否启动成功
try {
    $null = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✅ 后端服务健康检查通过" -ForegroundColor Green
} catch {
    Write-Host "⚠️  后端服务可能尚未完全启动，请稍后检查" -ForegroundColor Yellow
}

# 启动前端服务
Write-Host "`n🎯 启动前端服务器..." -ForegroundColor Yellow

# 检查前端依赖
if (-not (Test-Path "frontend\node_modules")) {
    Write-Host "🔧 安装前端依赖..." -ForegroundColor Cyan
    Push-Location frontend
    npm install
    Pop-Location
    Write-Host "✅ 前端依赖安装完成" -ForegroundColor Green
}

# 启动前端
$frontendProcess = Start-Process -FilePath "npm" -ArgumentList "run dev" -WorkingDirectory "$PWD.Path\frontend" -RedirectStandardOutput "logs\frontend.log" -RedirectStandardError "logs\frontend_error.log" -PassThru
Write-Host "✅ 前端服务器已启动 (端口: 3000, PID: $($frontendProcess.Id))" -ForegroundColor Green

# 等待前端启动
Start-Sleep -Seconds 5

# 启动浏览器
Write-Host "`n🌐 启动浏览器..." -ForegroundColor Yellow
Start-Process "http://localhost:3000"

Write-Host "`n🎉 AI销售教练系统启动完成！" -ForegroundColor Green
Write-Host "📊 系统访问地址:" -ForegroundColor Cyan
Write-Host "   前端界面: http://localhost:3000" -ForegroundColor White
Write-Host "   后端API:  http://localhost:8000" -ForegroundColor White
Write-Host "`n📋 日志文件位置:" -ForegroundColor Cyan
Write-Host "   前端日志: logs/frontend.log" -ForegroundColor White
Write-Host "   后端日志: logs/backend.log" -ForegroundColor White
Write-Host "`n⏹️  停止服务时，请关闭所有命令行窗口或按 Ctrl+C" -ForegroundColor Yellow