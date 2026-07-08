@echo off
REM ASMEBEL Bot - Windows Batch Starter
REM This script starts the bot with proper error handling

cls
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║     ASMEBEL Bot Launcher                         ║
echo ║     Bot o'rnatish va ishga tushirish             ║
echo ╚══════════════════════════════════════════════════╝
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python topilmadi! Iltimos Python 3.8+ o'rnatib qo'ying.
    echo https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python topildi!
echo.

REM Check if requirements are installed
echo 📦 Zotizlarni tekshiryapman...
pip show python-telegram-bot >nul 2>&1
if errorlevel 1 (
    echo ⚠️ Zotizlar o'rnatilmagan! O'rnatishni boshlayapman...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Zotizlarni o'rnatishda xatolik yuz berdi!
        pause
        exit /b 1
    )
    echo ✅ Zotizlar o'rnatildi!
) else (
    echo ✅ Barcha zotizlar o'rnatilgan!
)

echo.
echo 🚀 Bot ishga tushirilmoqda...
echo ============================================
echo.
echo Bilan bog'lanish:
echo - /start - Bot bilan tanishish
echo - /katalog - Katalog ko'rish
echo - /admin - Admin panel (faqat admin uchun)
echo.
echo Bot to'xtatish uchun: CTRL + C
echo.
echo ============================================
echo.

REM Start the bot
python bot.py

REM If bot exits
echo.
echo ⚠️ Bot to'xtadi.
echo Xatolik bo'lsa, @ilyosdesign2927 ga murojaat qiling.
pause
