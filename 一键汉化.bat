@echo off
chcp 65001 >nul
title Antigravity 一键汉化补丁
cd /d "%~dp0"
echo 正在运行 Antigravity 汉化补丁...
python Antigravity-Patcher.py
pause
