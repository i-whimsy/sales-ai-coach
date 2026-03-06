@echo off
chcp 65001 >nul
echo ==============================================
echo 🛑 停止AI销售教练系统
echo ==============================================
echo.

REM 停止前端服务
echo 🎯 停止前端服务器...
tasklist /fi "IMAGENAME eq node.exe" /fo csv | findstr "npm" >nul 2>&1
if %errorlevel% equ 0 (
    taskkill /f /im node.exe
    echo ✅ 前端服务器已停止
) else (
    echo ⚠️  前端服务器可能已经停止
)

REM 停止后端服务
echo.
echo 🎯 停止后端服务器...
tasklist /fi "IMAGENAME eq python.exe" /fo csv | findstr "main.py" >nul 2>&1
if %errorlevel% equ 0 (
    taskkill /f /im python.exe
    echo ✅ 后端服务器已停止
) else (
    echo ⚠️  后端服务器可能已经停止
)

REM 清理残留进程
echo.
echo 🧹 清理残留进程...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
echo ✅ 残留进程已清理

echo.
echo ==============================================
echo ✅ AI销售教练系统已完全停止
echo ==============================================
echo
pause