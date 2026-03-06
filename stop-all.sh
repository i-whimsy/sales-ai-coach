#!/bin/bash
set -euo pipefail

# AI销售教练系统停止脚本
# Shell版本 (Linux/macOS)

echo "==============================================="
echo "🛑 停止AI销售教练系统"
echo "==============================================="
echo

# 停止前端服务
echo "🎯 停止前端服务器..."
if [ -f "logs/frontend.pid" ]; then
    FRONTEND_PID=$(cat logs/frontend.pid)
    if kill -0 $FRONTEND_PID >/dev/null 2>&1; then
        kill $FRONTEND_PID
        echo "✅ 前端服务器已停止 (PID: $FRONTEND_PID)"
    else
        echo "⚠️  前端服务器可能已经停止"
    fi
    rm -f logs/frontend.pid
else
    echo "⚠️  未找到前端进程文件"
fi

# 停止后端服务
echo
echo "🎯 停止后端服务器..."
if [ -f "logs/backend.pid" ]; then
    BACKEND_PID=$(cat logs/backend.pid)
    if kill -0 $BACKEND_PID >/dev/null 2>&1; then
        kill $BACKEND_PID
        echo "✅ 后端服务器已停止 (PID: $BACKEND_PID)"
    else
        echo "⚠️  后端服务器可能已经停止"
    fi
    rm -f logs/backend.pid
else
    echo "⚠️  未找到后端进程文件"
fi

# 清理残留进程
echo
echo "🧹 清理残留进程..."
# 查找并清理Python和Node.js进程
ps aux | grep -E "(python.*main\.py|npm run dev)" | grep -v grep | awk '{print $2}' | xargs -r kill 2>/dev/null || true
echo "✅ 残留进程已清理"

echo
echo "==============================================="
echo "✅ AI销售教练系统已完全停止"
echo "==============================================="
echo