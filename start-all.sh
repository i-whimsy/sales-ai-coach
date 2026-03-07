#!/bin/bash
set -euo pipefail

# AI销售教练系统一键启动脚本
# Shell版本 (Linux/macOS)

echo "==============================================="
echo "🚀 AI销售教练系统一键启动脚本"
echo "==============================================="
echo

# 检查Python是否可用
echo "🔍 检查Python环境..."
if command -v python3 >/dev/null 2>&1; then
    echo "✅ Python环境已检测"
    PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
    echo "✅ Python环境已检测"
    PYTHON="python"
else
    echo "❌ 未找到Python，请先安装Python"
    exit 1
fi

# 检查Node.js是否可用
echo
echo "🔍 检查Node.js环境..."
if command -v node >/dev/null 2>&1; then
    echo "✅ Node.js环境已检测"
else
    echo "❌ 未找到Node.js，请先安装Node.js"
    exit 1
fi

# 创建输出目录
mkdir -p logs

# 启动后端服务
echo
echo "🎯 启动后端服务器..."

# 检查后端依赖
if [ ! -d "backend/venv" ]; then
    echo "🔧 创建并配置虚拟环境..."
    $PYTHON -m venv backend/venv
    source backend/venv/bin/activate
    pip install -r backend/requirements.txt
    deactivate
    echo "✅ 虚拟环境配置完成"
fi

# 启动后端
cd backend
source venv/bin/activate
nohup python main.py > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
echo $BACKEND_PID > ../logs/backend.pid
deactivate
cd ..
echo "✅ 后端服务器已启动 (端口: 8000, PID: $BACKEND_PID)"

# 等待后端启动
sleep 3

# 检查后端是否启动成功
echo
echo "🔍 检查后端服务..."
if curl -s -f -m 5 http://localhost:8000/health >/dev/null; then
    echo "✅ 后端服务健康检查通过"
else
    echo "⚠️  后端服务可能尚未完全启动，请稍后检查"
fi

# 启动前端服务
echo
echo "🎯 启动前端服务器..."

# 检查前端依赖
if [ ! -d "frontend-vue/node_modules" ]; then
    echo "🔧 安装前端依赖..."
    cd frontend-vue
    npm install
    cd ..
    echo "✅ 前端依赖安装完成"
fi

# 启动前端
cd frontend-vue
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
echo $FRONTEND_PID > ../logs/frontend.pid
cd ..
echo "✅ 前端服务器已启动 (端口: 3002, PID: $FRONTEND_PID)"

# 等待前端启动
sleep 5

# 启动浏览器
echo
echo "🌐 启动浏览器..."
if command -v open >/dev/null 2>&1; then
    open http://localhost:3002
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:3002
else
    echo "⚠️  请手动在浏览器中访问: http://localhost:3002"
fi

echo
echo "==============================================="
echo "🎉 AI销售教练系统启动完成！"
echo "==============================================="
echo
echo "📊 系统访问地址:"
echo "   前端界面: http://localhost:3002"
echo "   后端API:  http://localhost:8000"
echo
echo "📋 日志文件位置:"
echo "   前端日志: logs/frontend.log"
echo "   后端日志: logs/backend.log"
echo
echo "📝 进程信息:"
echo "   后端PID: $BACKEND_PID"
echo "   前端PID: $FRONTEND_PID"
echo
echo "⏹️  停止服务: ./stop-all.sh"
echo "==============================================="
echo