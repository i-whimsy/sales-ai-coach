# AI销售教练系统 - 自动提交到GitHub
# PowerShell版本

param(
    [string]$message = "Update: 自动提交代码到GitHub"
)

Write-Host "🚀 提交代码到GitHub..." -ForegroundColor Cyan

# 检查Git是否可用
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ 未找到Git，请先安装Git" -ForegroundColor Red
    exit 1
}

# 检查是否在Git仓库中
if (-not (Test-Path ".git")) {
    Write-Host "❌ 当前目录不是Git仓库" -ForegroundColor Red
    exit 1
}

# 检查远程仓库配置
try {
    $remote = git remote get-url origin
    Write-Host "✅ 远程仓库: $remote" -ForegroundColor Green
} catch {
    Write-Host "⚠️  未配置远程仓库，正在配置..." -ForegroundColor Yellow
    git remote add origin git@github.com:i-whimsy/sales-ai-coach.git
    Write-Host "✅ 配置远程仓库: git@github.com:i-whimsy/sales-ai-coach.git" -ForegroundColor Green
}

# 添加所有更改
Write-Host "🔧 添加所有更改..." -ForegroundColor Cyan
git add .

# 提交更改
Write-Host "📝 提交更改..." -ForegroundColor Cyan
git commit -m "$message"

# 推送到GitHub
Write-Host "🌐 推送到GitHub..." -ForegroundColor Cyan
try {
    git push origin master
    Write-Host "✅ 代码已成功提交到GitHub" -ForegroundColor Green
    Write-Host "📊 GitHub仓库: https://github.com/i-whimsy/sales-ai-coach" -ForegroundColor Cyan
} catch {
    Write-Host "⚠️  推送失败，尝试使用HTTPS方式..." -ForegroundColor Yellow
    git remote remove origin
    git remote add origin https://github.com/i-whimsy/sales-ai-coach.git
    try {
        git push origin master
        Write-Host "✅ 代码已成功通过HTTPS提交到GitHub" -ForegroundColor Green
    } catch {
        Write-Host "❌ 推送失败，请检查网络连接或GitHub配置" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n🎉 提交完成！" -ForegroundColor Green
Write-Host "📋 提交信息: $message" -ForegroundColor White