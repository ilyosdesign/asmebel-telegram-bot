# Render.com'ga Deploy Qo'llanma

## 🚀 Boshlang'ich o'rnatish

### 1. GitHub'ga yukla
```bash
git init
git add .
git commit -m "ASMEBEL Telegram Bot - Render uchun tayyor"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/asmebel-telegram-bot.git
git push -u origin main
```

### 2. Render.com'da yangi Web Service yaratish

1. **Render.com'ga kirish** - https://render.com (Sign Up)
2. **Dashboard** → **New** → **Web Service**
3. **Connect repository** - GitHub repo'sini tanlang
4. **Settings:**
   - **Name:** `asmebel-telegram-bot`
   - **Runtime:** `Python 3.11`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Plan:** Free (Bepul)

### 3. Environment Variables o'rnatish

**Render dashboard'da:**
1. **Environment** section'ga o'tish
2. Quyidagi o'zgaruvchilarni qo'shish:

```
TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
ADMIN_ID=YOUR_ADMIN_ID
ADMIN_USERNAME=YOUR_USERNAME
```

### 4. Deploy qilish

1. **Create Web Service** bosing
2. Render avtomatik build va deploy qiladi
3. **Deployment** bo'ladi (3-5 daqiqa)
4. Bot **24/7 online** bo'ladi! ✅

---

## 📝 Ma'lumotlarni qayerdan olish

### Telegram Bot Token
- **@BotFather** ga yozing Telegram'da
- `/newbot` yo'li bilan yangi bot yaratish
- Token nusxalang va `.env`'ga qo'ying

### Gemini API Key
- https://ai.google.dev/aistudio ga o'tish
- **Google account** bilan kirish
- **API key** yaratish va nusxalang

### Admin ID
- Bot'ga `/start` yuboring
- Logs'da o'zingizning `user_id` ko'rish mumkin
- Yoki @userinfobot'ga yozing

---

## 🔧 Local'da test qilish

Deploy qilishdan avval local'da test qiling:

```bash
# Virtual environment yaratish
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Dependencies o'rnatish
pip install -r requirements.txt

# .env fayli yaratish (root'da)
echo "TELEGRAM_TOKEN=your_token_here" > .env
echo "GEMINI_API_KEY=your_key_here" >> .env
echo "ADMIN_ID=your_id" >> .env
echo "ADMIN_USERNAME=your_username" >> .env

# Bot ishga tushirish
python bot.py
```

---

## 🎯 Render bepul plan haqida

✅ **Bepul paketda:**
- Unlimited Web Services
- 750 soat/oy ishga tushish (24/7 = 720 soat - OK!)
- 50GB ishga tushish storage
- Bepul SSL sertifikat

⚠️ **Cheklash:**
- 15 daqiqa inaktiv bo'lsa, sleep rejimiga o'tadi
- Sleep'dan chiqish 30 soniya vaqt oladi

---

## 📊 Bot ishlashini tekshirish

Deploy bo'lgandan so'ng:
1. **Render dashboard'da** logs ni ko'rish
2. Bot'ga `/start` yuboring Telegram'da
3. Agar javob bo'lsa - **Success!** ✅

---

## 🆘 Agar muammolar bo'lsa

### Bot javob bermaydi
- Render logs ni ko'ring: **Logs** tab
- `TELEGRAM_TOKEN` to'g'ri kiritilganmi?
- `GEMINI_API_KEY` to'g'ri kiritilganmi?

### Deploy qo'za olmadi
- `requirements.txt` to'g'ri bo'lganmi?
- `Procfile` mavjudmi?
- Syntax xatosi bo'lganmi?

---

## ✅ Deploy muvaffaqiyatli bo'ldi - Keyingi qadamlar

1. Bot test qiling
2. Mahsulotlar qo'shish
3. Foydalanuvchilar qo'shish
4. Admin funktsiyalarini tekshirish

---

**Tayyormisiz? Boshlashga o'xshaysizmi?** 🚀
