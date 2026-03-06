@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set MESSAGE=%~1
if "%MESSAGE%"=="" set MESSAGE=Update: 自动提交代码到GitHub

echo ===============================================
echo 🚀 提交代码到GitHub
echo ===============================================
echo.

REM 检查Git是否可用
where git >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 未找到Git，请先安装Git
    pause
    exit /b 1
)

REM 检查是否在Git仓库中
if not exist ".git" (
    echo ❌ 当前目录不是Git仓库
    pause
    exit /b 1
)

REM 检查远程仓库配置
echo 🔍 检查远程仓库...
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    git remote get-url origin | findstr /r "^.*$" >nul
    echo ✅ 远程仓库: !errorlevel!
) else (
    echo ⚠️  未配置远程仓库，正在配置...
    git remote add origin git@github.com:i-whimsy/sales-ai-coach.git
    echo ✅ 配置远程仓库: git@github.com:i-whimsy/sales-ai-coach.git
)

REM 添加所有更改
echo.
echo 🔧 添加所有更改...
git add .

REM 提交更改
echo.
echo 📝 提交更改...
git commit -m "%MESSAGE%"

REM 推送到GitHub
echo.
echo 🌐 推送到GitHub...
git push origin master
if %errorlevel% neq 0 (
    echo ⚠️  SSH方式推送失败，尝试使用HTTPS方式...
    git remote remove origin
    git remote add origin https://github.com/i-whimsy/sales-ai-coach.git
    git push origin master
    if %errorlevel% equ 0 (
        echo ✅ 代码已成功通过HTTPS提交到GitHub
    ) else (
        echo ❌ 推送失败，请检查网络连接或GitHub配置
        pause
        exit /b 1
    )
) else (
    echo ✅ 代码已成功提交到GitHub
)

echo.
echo ===============================================
echo 🎉 提交完成！
echo ===============================================
echo.
echo 📋 提交信息: %MESSAGE%
echo 📊 GitHub仓库: https://github.com/i-whimsy/sales-ai-coach
echo.
pause