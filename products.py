# products.py

import json
import os
import time
"""
Mahsulotlar uchun yagona ma'lumot manbasi.
Bu fayl mahsulotlar haqidagi barcha ma'lumotlarni markazlashtiradi,
takrorlanishning oldini oladi va ma'lumotlarni boshqarishni osonlashtiradi.
"""

DATA_FILE = 'data.json'

# Asosiy ma'lumotlar strukturasi (fayl mavjud bo'lmasa ishlatiladi)
DEFAULT_DATA = {
    'kitchen': {'name': 'Oshxona mebellari', 'emoji': '🍽️', 'products': []},
    'bedroom': {'name': 'Yotoqxona mebellari', 'emoji': '🛏️', 'products': []},
    'tv_zone': {'name': 'TV Zonalar', 'emoji': '📺', 'products': []},
    'wardrobe': {'name': 'Gardiroblar', 'emoji': '🚪', 'products': []},
    'office': {'name': 'Ofis mebellari', 'emoji': '💼', 'products': []},
}

def load_data():
    """JSON fayldan ma'lumotlarni yuklaydi. Agar fayl bo'lmasa, uni yaratadi."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_DATA, f, ensure_ascii=False, indent=4)
        return DEFAULT_DATA
    
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        # Fayl bo'sh yoki xato bo'lsa, standart ma'lumotlarni qaytaramiz
        return DEFAULT_DATA

def save_data(data):
    """Ma'lumotlarni JSON faylga saqlaydi."""
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# Dastur ishga tushganda ma'lumotlarni yuklab olamiz
CATEGORIES_DATA = load_data()

def add_product(category_key: str, photo_id: str, caption: str):
    """Yangi mahsulotni ma'lumotlar bazasiga qo'shadi va faylga saqlaydi."""
    if category_key in CATEGORIES_DATA:
        new_product = {
            'id': int(time.time()), # Unikal ID uchun vaqtdan foydalanamiz
            'photo_id': photo_id,
            'caption': caption
        }
        CATEGORIES_DATA[category_key]['products'].append(new_product)
        save_data(CATEGORIES_DATA)

def add_category(category_key: str, category_name: str, emoji: str) -> bool:
    """Yangi kategoriyani qo'shadi va faylga saqlaydi."""
    # Kategoriya kaliti mavjud emasligini va bo'sh emasligini tekshirish
    if category_key in CATEGORIES_DATA or not category_key.strip():
        return False
    CATEGORIES_DATA[category_key] = {
        'name': category_name,
        'emoji': emoji,
        'products': []
    }
    save_data(CATEGORIES_DATA)
    return True

def delete_category(category_key: str) -> bool:
    """Mavjud kategoriyani o'chiradi va faylni saqlaydi."""
    if category_key in CATEGORIES_DATA:
        # Kategoriyani o'chirish
        # Faqat bo'sh kategoriyalarni o'chirishga ruxsat berish yaxshiroq, lekin hozircha oddiy o'chiramiz
        del CATEGORIES_DATA[category_key]
        save_data(CATEGORIES_DATA)
        return True
    return False

def edit_product(category_key: str, product_id: int, new_data: dict) -> bool:
    """Mahsulotni ID bo'yicha tahrirlaydi va faylni saqlaydi."""
    if category_key in CATEGORIES_DATA:
        products = CATEGORIES_DATA[category_key].get('products', [])
        product_to_edit = next((p for p in products if p.get('id') == product_id), None)
        if product_to_edit:
            # Update with new photo_id or caption
            product_to_edit.update(new_data)
            save_data(CATEGORIES_DATA)
            return True
    return False

def delete_product(category_key: str, product_id: int) -> bool:
    """Mahsulotni ID bo'yicha o'chiradi va faylni saqlaydi."""
    if category_key in CATEGORIES_DATA:
        products = CATEGORIES_DATA[category_key].get('products', [])
        # O'chiriladigan mahsulotni topib, ro'yxatdan olib tashlash
        product_to_delete = next((p for p in products if p.get('id') == product_id), None)
        if product_to_delete:
            products.remove(product_to_delete)
            save_data(CATEGORIES_DATA)
            return True
    return False

def get_categories_for_prompt() -> str:
    """Gemini uchun mavjud kategoriya ro'yxatini matn formatida tayyorlaydi."""
    category_names = [cat['name'] for cat in CATEGORIES_DATA.values()]
    return f"Bizning asosiy mebel turlarimiz: {', '.join(category_names)}."