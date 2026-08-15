# user_manager.py

import json
import os
import logging

logger = logging.getLogger(__name__)

USERS_FILE = 'users.json'

def get_all_user_ids():
    if not os.path.exists(USERS_FILE):
        return []

    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, list):
                logger.warning("users.json formatida xatolik, massiv emas")
                return []
            return data
    except json.JSONDecodeError as e:
        logger.error(f"users.json JSON xatoligi: {e}")
        return []
    except Exception as e:
        logger.error(f"users.json o'qishda xatolik: {e}")
        return []

def add_user(user_id: int):
    if not isinstance(user_id, (int, str)):
        logger.warning(f"Noto'g'ri user_id tipi: {type(user_id)}")
        return False

    user_id = int(user_id)

    try:
        user_ids = get_all_user_ids()
        if user_id not in user_ids:
            user_ids.append(user_id)
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(user_ids, f, indent=4)
            logger.info(f"Foydalanuvchi qo'shildi: {user_id}")
            return True
        return False
    except Exception as e:
        logger.error(f"Foydalanuvchini saqlashda xatolik: {e}")
        return False