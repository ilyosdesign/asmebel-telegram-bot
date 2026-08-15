# 🚀 ASMEBEL Telegram Bot - Deployment Guide

## Tezkor O'rnatish (Render.com)

### 1. Render'da Deploy Qilish

**Qadam 1: Repository GitHub'da**
```bash
git push origin main
```

**Qadam 2: Render.com'ga kiring**
- https://render.com ga kirish
- "New +" → "Web Service" tanlash
- GitHub repository'ni ulash (ilyosdesign/asmebel-telegram-bot)

**Qadam 3: Sozlamalarni qo'yish**
```
Nomi: asmebel-bot
Muhit: Python 3
Build Command: pip install -r requirements.txt
Start Command: python bot.py
```

**Qadam 4: Environment Variables qo'yish**

Render dashboard'da "Environment" → Add qilish:
```
TELEGRAM_TOKEN = your_token_here
GEMINI_API_KEY = your_api_key_here
ADMIN_ID = 8591485024
ADMIN_USERNAME = ilyosdesign2927
WEBAPP_URL = https://your-app.render.com
PORT = 10000
```

**Qadam 5: Deploy qilish**
- "Deploy" tugmasini bosish
- Kutish (2-3 minut)
- ✅ Deployed!

---

## 📱 Telegram Bot Webhook Sozlash

Deploy qilingandan keyin:

```bash
# Bot URLni olish (Render dashboard'dan)
# https://asmebel-bot.onrender.com/

# Webhook o'rnatish
curl -X POST https://api.telegram.org/bot{TELEGRAM_TOKEN}/setWebhook \
  -H'Content-Type: application/json' \
  -d '{"url":"https://asmebel-bot.onrender.com/webhook"}'
```

---

## 🔒 Security Checklist

- [x] .env fayli `.gitignore` da
- [x] Tokenlar Render Environment'da
- [x] HTTPS ishlatilmoqda (Render automatic)
- [x] Admin ID majburiy
- [x] Input validation qo'shilgan
- [x] Error handling yaxshilangan
- [x] Logging enabled

---

## 📊 Monitoring

**Bot ishlashini tekshirish:**

1. Telegram bot'ga `/start` yuborish
2. Render dashboard'dan logs ko'rish
3. Excel faylida buyurtmalar ko'rish

**Logs ko'rish:**
```bash
# Render CLI orqali (optional)
render logs asmebel-bot
```

---

## 🐛 Debugging

**Local'da test qilish:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python bot.py
```

**Xatoliklar:**
- Port 3010 busy → Render PORT=10000 ishlatadi (to'g'ri)
- HTTPS kerak → Render automatic qiladi (to'g'ri)
- Tokens missing → Environment variables tekshirish

---

## 📈 Future Improvements

- [ ] Google Gemini API'ni yangi package'ga o'tkazish
- [ ] WebApp interfeys Render'da host qilish
- [ ] Database (PostgreSQL) qo'shish
- [ ] Admin stats dashboard
- [ ] Multi-language support

---

## 📞 Support

**Muammolar:**
1. Telegram token to'g'rimi?
2. GEMINI_API_KEY validi?
3. ADMIN_ID to'g'rimi?
4. Port 10000 Render uchun configured?

**Bot Test:**
```bash
python final_check.py
```

---

**Status:** ✅ DEPLOYMENT TAYYOR

**Last Updated:** 2026-08-15

**Version:** 1.0.0 Production Ready
