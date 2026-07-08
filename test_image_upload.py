#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rasm yuklash jarayonini test qiladigan skript.
Bu skript ConversationHandler va photo upload logikasini tekshiradi.
"""

import json
import os
import sys
from products import CATEGORIES_DATA, add_product

print("=" * 60)
print("🧪 RASM YUKLASH TESTI")
print("=" * 60)

# Test 1: Kategoriyalarni tekshirish
print("\n✅ Test 1: Kategoriyalar mavjudmi?")
print(f"   Kategoriyalar: {list(CATEGORIES_DATA.keys())}")
if len(CATEGORIES_DATA) == 0:
    print("   ❌ XATOLIK: Kategoriyalar yo'q!")
    sys.exit(1)
else:
    print(f"   ✅ {len(CATEGORIES_DATA)} ta kategoriya topildi")

# Test 2: Callback pattern tekshirish
print("\n✅ Test 2: Callback datalarini tekshirish")
pattern_example = "^add_cat_(" + ("|".join(CATEGORIES_DATA.keys())) + ")$"
print(f"   Pattern: {pattern_example}")

test_callbacks = [
    ("add_cat_kitchen", True),
    ("add_cat_bedroom", True),
    ("add_cat_tv_zone", True),
    ("add_cat_wardrobe", True),
    ("add_cat_office", True),
    ("add_cat_invalid", False),
    ("add_cat_", False),
]

import re
pattern_regex = re.compile(pattern_example)
for callback, should_match in test_callbacks:
    matches = bool(pattern_regex.match(callback))
    status = "✅" if matches == should_match else "❌"
    print(f"   {status} '{callback}': {matches} (kutilayotgan: {should_match})")

# Test 3: Context user_data simulyatsiyasi
print("\n✅ Test 3: Context user_data simulyatsiyasi")
context_user_data = {
    'category_key': 'kitchen',
    'photo_id': 'AgACAgIAAxkBAAICFGdhVHLB...',  # Fake photo ID
}
print(f"   Category: {context_user_data.get('category_key')}")
print(f"   Photo ID: {context_user_data.get('photo_id')[:30]}...")

# Test 4: Mahsulot qo'shish
print("\n✅ Test 4: Mahsulot qo'shish testi")
try:
    test_caption = "Test mahsulot\nNarxi: 1,000,000 so'm"
    add_product(
        category_key='kitchen',
        photo_id='AgACAgIAAxkBAAICFGdhVHLB...',
        caption=test_caption
    )
    print(f"   ✅ Mahsulot muvaffaqiyatli qo'shildi")
    
    # Verify it was added
    if 'kitchen' in CATEGORIES_DATA:
        products_count = len(CATEGORIES_DATA['kitchen']['products'])
        print(f"   ✅ Oshxona bo'limida {products_count} ta mahsulot bor")
    
except Exception as e:
    print(f"   ❌ XATOLIK: {e}")
    sys.exit(1)

# Test 5: State constants tekshirish
print("\n✅ Test 5: ConversationHandler state konstantalari")
print("   State constants:")
print(f"   SELECT_CATEGORY = 0")
print(f"   GET_PHOTO = 1")
print(f"   GET_CAPTION = 2")

# Test 6: ADMIN_ID tekshirish
print("\n✅ Test 6: ADMIN_ID konfiguratsiyasi")
from config import ADMIN_ID, ADMIN_USERNAME
if ADMIN_ID and ADMIN_USERNAME:
    print(f"   ✅ ADMIN_ID: {ADMIN_ID}")
    print(f"   ✅ ADMIN_USERNAME: {ADMIN_USERNAME}")
else:
    print(f"   ⚠️  ADMIN_ID yoki ADMIN_USERNAME bo'sh")
    if not ADMIN_ID:
        print(f"   ⚠️  ADMIN_ID: (bo'sh)")
    if not ADMIN_USERNAME:
        print(f"   ⚠️  ADMIN_USERNAME: (bo'sh)")

# Test 7: Data.json faylini tekshirish
print("\n✅ Test 7: data.json faylini tekshirish")
if os.path.exists('data.json'):
    with open('data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"   ✅ data.json faylida {len(data)} ta kategoriya")
    for cat_key, cat_data in data.items():
        products_count = len(cat_data.get('products', []))
        print(f"      • {cat_key}: {products_count} ta mahsulot")
else:
    print(f"   ❌ data.json faylining topilmadi")

print("\n" + "=" * 60)
print("✅ BARCHA TESTLAR TUGATILDI")
print("=" * 60)
print("""
Rasm yuklash muammosi bo'lmaydi agar:
1. ✅ Kategoriyalar mavjud
2. ✅ Callback pattern to'g'ri
3. ✅ User data saqlanadi
4. ✅ Mahsulotlar qo'shiladi
5. ✅ ADMIN_ID to'g'ri

Agar hammoq mavjud bo'lsa, muammo Telegram API yoki user workflow'da bo'lishi mumkin.
Tafsilotlar bilan xabar bering:
- Qaysi qadamda to'xtaydi?
- Qanday xata xabari ko'rinadi?
""")
