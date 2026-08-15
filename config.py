# config.py

import os
from dotenv import load_dotenv

# .env faylidan o'zgaruvchilarni yuklash
load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_ID = os.getenv("ADMIN_ID", "").strip()
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "").strip()
WEBAPP_URL = os.getenv("WEBAPP_URL", "").strip()
PORT = os.getenv("PORT", "8080")

if not TELEGRAM_TOKEN or not GEMINI_API_KEY:
    raise ValueError("Iltimos, .env fayliga TELEGRAM_TOKEN va GEMINI_API_KEY'ni to'liq kiriting.")

if not ADMIN_ID or not ADMIN_USERNAME:
    raise ValueError("ADMIN_ID va ADMIN_USERNAME majburiy parametrlar. Iltimos, .env faylida ko'rsating.")
