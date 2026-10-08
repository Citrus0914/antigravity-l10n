@echo off
chcp 65001 >nul
title Antigravity 一键还原工具
cd /d "%~dp0"
echo 正在运行 Antigravity 还原工具...
python Restore.py
pause
