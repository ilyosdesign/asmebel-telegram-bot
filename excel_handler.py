# excel_handler.py

import os
from datetime import datetime
from openpyxl import Workbook, load_workbook

ORDERS_FILE = 'buyurtmalar.xlsx'
HEADERS = [
    'Vaqt', 'Mijoz ID', 'Mijoz Username', 'Mijoz Ismi', 'Telefon Raqam', 'Mahsulot Nomi'
]

def setup_excel_file():
    """
    Agar 'buyurtmalar.xlsx' fayli mavjud bo'lmasa, uni yaratadi va sarlavhalarni qo'shadi.
    """
    if not os.path.exists(ORDERS_FILE):
        workbook = Workbook()
        sheet = workbook.active
        if sheet:
            sheet.title = "Buyurtmalar"
            sheet.append(HEADERS)
            workbook.save(ORDERS_FILE)

def save_order_to_excel(user_data: dict, product_name: str):
    """
    Yangi buyurtmani Excel fayliga qo'shadi.
    """
    try:
        setup_excel_file() # Fayl mavjudligini tekshirish
        workbook = load_workbook(ORDERS_FILE)
        sheet = workbook.active

        if sheet:
            order_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            new_row = [
                order_time,
                user_data.get('id'),
                user_data.get('username'),
                user_data.get('full_name'),
                user_data.get('phone_number'),
                product_name
            ]
            sheet.append(new_row)
            workbook.save(ORDERS_FILE)
    except Exception as e:
        print(f"Excelga yozishda xatolik: {e}")