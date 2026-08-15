@echo off
title ASMEBEL Bot - Restart
color 0A
echo.
echo ============================================
echo   ASMEBEL Bot - Barcha eski jarayonlarni
echo   to'xtatib, qayta ishga tushirish
echo ============================================
echo.

echo [1/3] Eski Python jarayonlarini to'xtatmoqdaman...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM python3.exe 2>nul
echo.

echo [2/3] 3 soniya kutilmoqda...
timeout /t 3 /nobreak >nul

echo [3/3] Botni qayta ishga tushirmoqdaman...
echo.
echo ============================================
echo  Bot ishga tushdi. To'xtatish uchun: CTRL+C
echo ============================================
echo.

python bot.py

echo.
echo Bot to'xtadi. Biror tugmani bosing...
pause
