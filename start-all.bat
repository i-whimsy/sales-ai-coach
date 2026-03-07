@echo off
chcp 65001 >nul
echo ==============================================
echo 🚀 AI销售教练系统一键启动脚本
echo ==============================================
echo.

REM 检查Python是否可用
echo 🔍 检查Python环境...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Python，请先安装Python
    pause
    exit /b 1
)
echo ✅ Python环境已检测

REM 检查Node.js是否可用
echo.
echo 🔍 检查Node.js环境...
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Node.js，请先安装Node.js
    pause
    exit /b 1
)
echo ✅ Node.js环境已检测

REM 创建输出目录
if not exist "logs" mkdir logs

REM 启动后端服务
echo.
echo 🎯 启动后端服务器...

REM 检查后端依赖
if not exist "backend\venv" (
    echo 🔧 创建并配置虚拟环境...
    python -m venv backend\venv
    call backend\venv\Scripts\activate.bat
    pip install -r backend\requirements.txt
    deactivate
    echo ✅ 虚拟环境配置完成
)

REM 启动后端
start "Backend Server" /MIN python backend\main.py
echo ✅ 后端服务器已启动 (端口: 8000)

REM 等待后端启动
timeout /t 3 /nobreak >nul

REM 检查后端是否启动成功
echo.
echo 🔍 检查后端服务...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ 后端服务健康检查通过
) else (
    echo ⚠️  后端服务可能尚未完全启动，请稍后检查
)

REM 启动前端服务
echo.
echo 🎯 启动前端服务器...

REM 检查前端依赖
if not exist "frontend-vue\node_modules" (
    echo 🔧 安装前端依赖...
    cd frontend-vue
    npm install
    cd ..
    echo ✅ 前端依赖安装完成
)

REM 启动前端
cd frontend-vue
start "Frontend Server" /MIN npm run dev
cd ..
echo ✅ 前端服务器已启动 (端口: 3002)

REM 等待前端启动
timeout /t 5 /nobreak >nul

REM 启动浏览器
echo.
echo 🌐 启动浏览器...
start http://localhost:3002

echo.
echo ==============================================
echo 🎉 AI销售教练系统启动完成！
echo ==============================================
echo.
echo 📊 系统访问地址:
echo    前端界面: http://localhost:3002
echo    后端API:  http://localhost:8000
echo.
echo 📋 日志文件位置:
echo    前端日志: logs/frontend.log
echo    后端日志: logs/backend.log
echo.
echo ⏹️  停止服务时，请关闭所有命令行窗口
echo ==============================================
echo.
pause