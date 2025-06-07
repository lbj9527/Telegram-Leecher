@echo off
chcp 65001 >nul
title Telegram Leecher Bot

echo.
echo ===============================================
echo         Telegram Leecher Bot 启动程序
echo ===============================================
echo.

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 错误: 未检测到Python
    echo 请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查配置文件
if not exist "credentials.json" (
    echo ❌ 错误: 找不到配置文件 credentials.json
    echo 请参考 credentials.json.example 创建配置文件
    echo.
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo 🚀 正在启动 Telegram Leecher Bot...
echo.

REM 启动Bot
python run.py

echo.
echo Bot已停止运行
pause 