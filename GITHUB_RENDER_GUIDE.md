# 🚀 GitHub'ga Upload va Render'da Deploy Qilish

## ⚡ 3 Qadam - 5 Daqiqa!

---

## **QADAM 1: GitHub'da Yangi Repository Yaratish**

1. **https://github.com/new** ga o'tish
2. **Repository name:** `asmebel-telegram-bot`
3. **Description:** `ASMEBEL Furniture Telegram Bot`
4. **Public** tanlash (bepul uchun)
5. **.gitignore:** Python tanlash
6. **Create repository** bosing

→ **Copy qilib oling:**
```
https://github.com/YOUR_USERNAME/asmebel-telegram-bot.git
```

---

## **QADAM 2: GitHub'ga Fayllarni Upload Qilish**

### **Usul 1: Web Interface orqali (ENG OSON)**

1. Yangi yaratilgan repo'siga o'tish
2. **Add file** → **Upload files**
3. **Bu fayllarni upload qiling:**

```
✅ bot.py
✅ config.py
✅ excel_handler.py
✅ faq.py
✅ gemini_handler.py
✅ products.py
✅ user_manager.py
✅ requirements.txt
✅ Procfile
✅ .env.example
✅ RENDER_DEPLOY.md
✅ README.md (agar kerak bo'lsa)
```

4. **Commit message:** `Initial commit - ASMEBEL Bot for Render`
5. **Commit changes** bosing

### **Usul 2: Git CLI orqali (Agar Git o'rnatilgan bo'lsa)**

```bash
cd "C:\Users\QuadroMi\Desktop\ASMEBEL BOT\asmebel-telegram-bot"

# Existing fayllarni stage qilish
git add .

# Commit qilish
git commit -m "ASMEBEL Bot - Render uchun tayyor"

# Remote add qilish
git branch -M main
git remote set-url origin https://github.com/YOUR_USERNAME/asmebel-telegram-bot.git

# Push qilish
git push -u origin main
```

---

## **QADAM 3: Render.com'da Deploy Qilish**

### **3.1 Render Account Yaratish**
1. **https://render.com** ga o'tish
2. **Sign up** → GitHub account bilan (eng oson)
3. Email verify qilish

### **3.2 Web Service Yaratish**
1. **Dashboard** → **New +** → **Web Service**
2. **Connect your repository** bosing
3. GitHub repo'sini tanlash (asmebel-telegram-bot)
4. **Connect** bosing

### **3.3 Deploy Settings**

```
Nom:                 asmebel-telegram-bot
Runtime:             Python 3.11
Root Directory:      (bo'sh qoldiring)
Build Command:       pip install -r requirements.txt
Start Command:       python bot.py
```

### **3.4 Environment Variables O'rnatish**

**Render'da Environment bo'limiga o'tish va qo'shish:**

```
Key: TELEGRAM_TOKEN
Value: (Bot token - @BotFather dan olingan)

Key: GEMINI_API_KEY
Value: (Google AI Key - ai.google.dev dan olingan)

Key: ADMIN_ID
Value: (Sizning Telegram ID - @userinfobot dan olingan)

Key: ADMIN_USERNAME
Value: (Sizning Telegram username - @ bilan)
```

### **3.5 Deploy Qilish**

1. **Create Web Service** bosing
2. Render avtomatik build qiladi (3-5 daqiqa)
3. ✅ **Live** bo'lganda - **BOT ONLINE!**

---

## 📋 Kerakli Ma'lumotlarni Topish

### **Telegram Bot Token**
```
1. Telegram'da @BotFather yozing
2. /newbot buyrug'ini yuboring
3. Bot nomini kiriting: ASMEBEL Bot
4. Username kiriting: asmebel_bot (yoki o'zingiznikini)
5. TOKEN nusxalang va .env'ga qo'ying
```

### **Gemini API Key**
```
1. https://ai.google.dev/aistudio ga o'tish
2. Google Account bilan kirish
3. "Get API key" bosing
4. "Create API key in new project" tanlang
5. Key nusxalang va .env'ga qo'ying
```

### **Admin ID**
```
Usul 1: @userinfobot'ga /start yuboring
Usul 2: Bot'ni run qilib, /start yuboring, logs'da ID ko'rish
```

---

## ✅ Deploy Muvaffaqiyatli Bo'ldi?

Bot test qiling:
```
1. Telegram'da bot nomini qidirish: @asmebel_bot (yoki siznikini)
2. /start yuboring
3. Javob kelsa - **SUCCESS!** ✅
```

---

## 🎯 Deploy After - Keyingi Qadamlar

1. ✅ Bot ishlayotganmi test qilish
2. ✅ /admin buyrug'ini tekshirish
3. ✅ Mahsulotlar qo'shish test qilish
4. ✅ Foydalanuvchilar chaqirib ko'rish

---

## 🆘 Agar Deploy Bo'za Olmasa

### **Xato: "Build failed"**
- `requirements.txt` to'g'ri bo'lganmi?
- `Procfile` mavjudmi?
- Python syntax xatosi bo'lganmi?

### **Xato: "Bot javob bermaydi"**
- Token to'g'ri kiritilganmi?
- API key to'g'ri kiritilganmi?
- Render logs'ni ko'ring

### **Xato: "Connection timeout"**
- Firewall yig'na qilayotganmi?
- Internet connection to'g'rimi?

---

## 📊 Render Bepul Plan

✅ **Nima bor:**
- 750 soat/oy (24/7 = 720 soat - Perfect!)
- Unlimited services
- 50GB storage
- Free SSL certificate

⚠️ **Cheklov:**
- 15 daqiqa inaktiv → sleep mode
- Sleep'dan wake-up: ~30 soniya

---

## 🎓 Render Logs Ni Ko'rish

1. **Render Dashboard** → Bot service
2. **Logs** tab'ni tanlash
3. **Real-time logs** ko'rish mumkin
4. Xatolarni topish

---

## 📱 Bot Ishlash Tekshirish

```bash
# Terminal/CMD da:
curl https://api.telegram.org/bot<YOUR_TOKEN>/getMe
# Javob bo'lsa - token to'g'ri ✅
```

---

**Tayyor? Boshlashga o'xshaysizmi?** 🚀

**ESLATMA:** Deploy qilgandan so'ng, bot **24/7** online bo'ladi. Render avtomatik restart qiladi. 

**Sizga kerak faqat:**
1. GitHub account (5 daqiqa)
2. Telegram bot token (@BotFather)
3. Gemini API key (Google AI Studio)
4. Render account (free)

**Hamma tayyor? Men qo'shimcha yordam beray olaman!** 💪
