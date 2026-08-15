# ASMEBEL Bot

🇺🇿 O'zbekcha Telegram bot - ASMEBEL mebel do'koniga buyurtmalar qabul qilish uchun.

## 🎯 Xususiyatlari

- 📱 Telegram Bot (Admin panel + Customer interface)
- 🤖 Gemini AI - Virtual yordamchi
- 🛋️ Katalog - 5 ta kategoriya mebeli
- 📦 Buyurtmalar - Excel'ga saqlanadi
- 🔐 Admin Funksiyalari - Mahsulot boshqarish
- 📊 WebApp - Interfeys

## ✅ Installed Features

- [x] Admin panel bilan mahsulot boshqarish
- [x] Kategoriya yaratish/o'chirish
- [x] Gemini AI - Virtual yordamchi
- [x] Excel buyurtmalar
- [x] Telegram WebApp
- [x] Security & Logging
- [x] Input Validation
- [x] Error Handling

## 🚀 Quick Start

### Local Development
```bash
# 1. Virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Dependencies
pip install -r requirements.txt

# 3. .env setup
cp .env.example .env
# .env faylida token'larni qo'yish

# 4. Bot ishga tushirish
python bot.py
```

### Render.com Deployment
[DEPLOYMENT.md](DEPLOYMENT.md) faylini ko'rish

## 📋 Environment Variables

```
TELEGRAM_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key
ADMIN_ID=your_admin_id
ADMIN_USERNAME=your_username
PORT=3010 (local) / 10000 (Render)
WEBAPP_URL=https://your-domain.com
```

## 📁 Struktura

```
asmebel-telegram-bot/
├── bot.py                 # Main bot logic
├── config.py              # Configuration
├── products.py            # Product management
├── gemini_handler.py      # AI responses
├── excel_handler.py       # Order export
├── user_manager.py        # User tracking
├── faq.py                 # FAQ data
├── requirements.txt       # Dependencies
├── Procfile              # Heroku/Render config
└── DEPLOYMENT.md         # Deploy instructions
```

## 🔐 Security

- ✅ Input validation
- ✅ Error handling
- ✅ Logging
- ✅ Admin verification
- ✅ Secure dependencies

## 📊 Testing

```bash
# Full system check
python final_check.py

# Simple bot test
python test_bot_simple.py
```

## 🤝 Development

**Last Update:** 2026-08-15
- Security improvements
- Better error handling
- Input validation
- Logging enhancements
- Production-ready

## 📞 Bot Commands

- `/start` - Bot ishga tushirish
- `/katalog` - Mebel katalogi
- `/admin` - Admin panel (admin'lar uchun)
- `/app` - Web interfeys

## 🎯 Status

**Production Ready**: ✅

---

**Made with ❤️ for ASMEBEL**
