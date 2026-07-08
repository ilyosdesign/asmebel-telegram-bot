# ASMEBEL Bot - PowerShell Starter
# This script starts the bot with proper error handling

Write-Host "`n" -ForegroundColor White
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     ASMEBEL Bot Launcher                         ║" -ForegroundColor Cyan
Write-Host "║     Bot o'rnatish va ishga tushirish             ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor White

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python topildi: $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host "❌ Python topilmadi! Iltimos Python 3.8+ o'rnatib qo'ying." -ForegroundColor Red
    Write-Host "https://www.python.org/downloads/" -ForegroundColor Yellow
    Read-Host "Davom ettirish uchun Enter tushmang"
    exit 1
}

Write-Host "`n" -ForegroundColor White

# Check if requirements are installed
Write-Host "📦 Zotizlarni tekshiryapman..." -ForegroundColor Yellow
$null = pip show python-telegram-bot 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️ Zotizlar o'rnatilmagan! O'rnatishni boshlayapman..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Zotizlarni o'rnatishda xatolik yuz berdi!" -ForegroundColor Red
        Read-Host "Davom ettirish uchun Enter tushmang"
        exit 1
    }
    Write-Host "✅ Zotizlar o'rnatildi!" -ForegroundColor Green
} else {
    Write-Host "✅ Barcha zotizlar o'rnatilgan!" -ForegroundColor Green
}

Write-Host "`n" -ForegroundColor White
Write-Host "🚀 Bot ishga tushirilmoqda..." -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor White

Write-Host "Bilan bog'lanish:" -ForegroundColor Green
Write-Host "- /start - Bot bilan tanishish" -ForegroundColor Green
Write-Host "- /katalog - Katalog ko'rish" -ForegroundColor Green
Write-Host "- /admin - Admin panel (faqat admin uchun)" -ForegroundColor Green
Write-Host "`n" -ForegroundColor White

Write-Host "Bot to'xtatish uchun: CTRL + C" -ForegroundColor Yellow
Write-Host "`n" -ForegroundColor White
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor White

# Start the bot
python bot.py

Write-Host "`n" -ForegroundColor White
Write-Host "⚠️ Bot to'xtadi." -ForegroundColor Yellow
Write-Host "Xatolik bo'lsa, @ilyosdesign2927 ga murojaat qiling." -ForegroundColor Yellow
Read-Host "Davom ettirish uchun Enter tushmang"
