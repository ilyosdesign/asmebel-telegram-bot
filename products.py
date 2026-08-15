# products.py

import json
import os
import time
import uuid
import logging

logger = logging.getLogger(__name__)

DATA_FILE = 'data.json'

DEFAULT_DATA = {
    'kitchen': {'name': 'Oshxona mebellari', 'emoji': '🍽️', 'products': []},
    'bedroom': {'name': 'Yotoqxona mebellari', 'emoji': '🛏️', 'products': []},
    'tv_zone': {'name': 'TV Zonalar', 'emoji': '📺', 'products': []},
    'wardrobe': {'name': 'Gardiroblar', 'emoji': '🚪', 'products': []},
    'office': {'name': 'Ofis mebellari', 'emoji': '💼', 'products': []},
}

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=4)
        return DEFAULT_DATA

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        logger.error("data.json ni o'qishda xatolik, standart ma'lumotlarni qaytarayapman")
        return DEFAULT_DATA

def save_data(data):
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    except Exception as e:
        logger.error(f"data.json ni saqlashda xatolik: {e}")

CATEGORIES_DATA = load_data()

def _generate_unique_id():
    return str(uuid.uuid4())[:8] + str(int(time.time() * 1000) % 10000)

def add_product(category_key: str, photo_id: str, caption: str):
    if not category_key or category_key not in CATEGORIES_DATA:
        logger.warning(f"Noto'g'ri kategoriya kaliti: {category_key}")
        return False

    if not photo_id or not caption:
        logger.warning("Photo ID yoki caption bo'sh")
        return False

    new_product = {
        'id': _generate_unique_id(),
        'photo_id': photo_id,
        'caption': caption.strip()
    }
    CATEGORIES_DATA[category_key]['products'].append(new_product)
    save_data(CATEGORIES_DATA)
    logger.info(f"Mahsulot qo'shildi: {category_key} -> {new_product['id']}")
    return True

def add_category(category_key: str, category_name: str, emoji: str) -> bool:
    if not category_key or not category_key.strip() or category_key in CATEGORIES_DATA:
        logger.warning(f"Kategoriya qo'shishda xatolik: {category_key}")
        return False

    if not category_name or not emoji:
        logger.warning("Kategoriya nomi yoki emoji bo'sh")
        return False

    CATEGORIES_DATA[category_key] = {
        'name': category_name.strip(),
        'emoji': emoji.strip(),
        'products': []
    }
    save_data(CATEGORIES_DATA)
    logger.info(f"Kategoriya qo'shildi: {category_key}")
    return True

def delete_category(category_key: str) -> bool:
    if category_key not in CATEGORIES_DATA:
        logger.warning(f"Kategoriya topilmadi: {category_key}")
        return False

    del CATEGORIES_DATA[category_key]
    save_data(CATEGORIES_DATA)
    logger.info(f"Kategoriya o'chirildi: {category_key}")
    return True

def edit_product(category_key: str, product_id: str, new_data: dict) -> bool:
    if category_key not in CATEGORIES_DATA:
        logger.warning(f"Noto'g'ri kategoriya: {category_key}")
        return False

    products = CATEGORIES_DATA[category_key].get('products', [])
    product = next((p for p in products if p.get('id') == product_id), None)

    if not product:
        logger.warning(f"Mahsulot topilmadi: {product_id}")
        return False

    if 'photo_id' in new_data and new_data['photo_id']:
        product['photo_id'] = new_data['photo_id']
    if 'caption' in new_data and new_data['caption']:
        product['caption'] = new_data['caption'].strip()

    save_data(CATEGORIES_DATA)
    logger.info(f"Mahsulot tahrirlandi: {product_id}")
    return True

def delete_product(category_key: str, product_id: str) -> bool:
    if category_key not in CATEGORIES_DATA:
        logger.warning(f"Noto'g'ri kategoriya: {category_key}")
        return False

    products = CATEGORIES_DATA[category_key].get('products', [])
    product = next((p for p in products if p.get('id') == product_id), None)

    if not product:
        logger.warning(f"Mahsulot topilmadi: {product_id}")
        return False

    products.remove(product)
    save_data(CATEGORIES_DATA)
    logger.info(f"Mahsulot o'chirildi: {product_id}")
    return True

def get_categories_for_prompt() -> str:
    try:
        category_names = [cat['name'] for cat in CATEGORIES_DATA.values()]
        return f"Bizning asosiy mebel turlarimiz: {', '.join(category_names)}."
    except Exception as e:
        logger.error(f"Kategoriyalarni olishda xatolik: {e}")
        return "Bizning mebel turlarini ko'rish uchun menyu bo'limiga o'ting."