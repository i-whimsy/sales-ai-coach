#!/bin/bash
set -euo pipefail

# AI销售教练系统 - 自动提交到GitHub
# Shell版本 (Linux/macOS)

MESSAGE="${1:-Update: 自动提交代码到GitHub}"

echo "==============================================="
echo "🚀 提交代码到GitHub"
echo "==============================================="
echo

# 检查Git是否可用
if ! command -v git >/dev/null 2>&1; then
    echo "❌ 未找到Git，请先安装Git" >&2
    exit 1
fi

# 检查是否在Git仓库中
if [ ! -d ".git" ]; then
    echo "❌ 当前目录不是Git仓库" >&2
    exit 1
fi

# 检查远程仓库配置
echo "🔍 检查远程仓库..."
if git remote get-url origin >/dev/null 2>&1; then
    echo "✅ 远程仓库: $(git remote get-url origin)"
else
    echo "⚠️  未配置远程仓库，正在配置..."
    git remote add origin git@github.com:i-whimsy/sales-ai-coach.git
    echo "✅ 配置远程仓库: git@github.com:i-whimsy/sales-ai-coach.git"
fi

# 添加所有更改
echo
echo "🔧 添加所有更改..."
git add .

# 提交更改
echo
echo "📝 提交更改..."
git commit -m "$MESSAGE"

# 推送到GitHub
echo
echo "🌐 推送到GitHub..."
if ! git push origin master; then
    echo "⚠️  SSH方式推送失败，尝试使用HTTPS方式..."
    git remote remove origin
    git remote add origin https://github.com/i-whimsy/sales-ai-coach.git
    if ! git push origin master; then
        echo "❌ 推送失败，请检查网络连接或GitHub配置" >&2
        exit 1
    fi
fi

echo
echo "==============================================="
echo "🎉 提交完成！"
echo "==============================================="
echo
echo "📋 提交信息: $MESSAGE"
echo "📊 GitHub仓库: https://github.com/i-whimsy/sales-ai-coach"
echo