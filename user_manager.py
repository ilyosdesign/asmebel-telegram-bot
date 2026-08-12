# user_manager.py

import json
import os

USERS_FILE = 'users.json'

def get_all_user_ids():
    """Barcha foydalanuvchi ID'larini JSON fayldan o'qiydi."""
    if not os.path.exists(USERS_FILE):
        return []
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def add_user(user_id: int):
    """Yangi foydalanuvchini ro'yxatga qo'shadi (agar u mavjud bo'lmasa)."""
    user_ids = get_all_user_ids()
    if user_id not in user_ids:
        user_ids.append(user_id)
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_ids, f, indent=4)
        except Exception as e:
            print(f"Foydalanuvchini saqlashda xatolik: {e}")