#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ASMEBEL Bot - Test Script
Проверка всех компонентов бота перед запуском
"""

import sys
import os
from pathlib import Path

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def print_status(message: str, status: bool):
    """Вывести статус проверки"""
    symbol = "✅" if status else "❌"
    print(f"{symbol} {message}")
    return status

def check_environment():
    """Проверить переменные окружения"""
    print("\n🔍 Проверка переменных окружения (.env)...\n")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    checks = []
    
    # Проверить TELEGRAM_TOKEN
    token = os.getenv("TELEGRAM_TOKEN")
    checks.append(print_status("TELEGRAM_TOKEN", bool(token)))
    
    # Проверить GEMINI_API_KEY
    gemini_key = os.getenv("GEMINI_API_KEY")
    checks.append(print_status("GEMINI_API_KEY", bool(gemini_key)))
    
    # Проверить ADMIN_ID
    admin_id = os.getenv("ADMIN_ID")
    checks.append(print_status("ADMIN_ID", bool(admin_id)))
    if admin_id:
        print(f"   └─ Admin ID: {admin_id}")
    
    # Проверить ADMIN_USERNAME
    admin_username = os.getenv("ADMIN_USERNAME")
    checks.append(print_status("ADMIN_USERNAME", bool(admin_username)))
    if admin_username:
        print(f"   └─ Admin Username: {admin_username}")
    
    return all(checks)

def check_dependencies():
    """Проверить установленные зависимости"""
    print("\n📦 Проверка зависимостей...\n")
    
    dependencies = [
        ("telegram", "python-telegram-bot"),
        ("google.generativeai", "google-generativeai"),
        ("dotenv", "python-dotenv"),
    ]
    
    checks = []
    for module, package_name in dependencies:
        try:
            __import__(module)
            checks.append(print_status(f"{package_name}", True))
        except ImportError:
            checks.append(print_status(f"{package_name}", False))
            print(f"   └─ Установка: pip install {package_name}")
    
    return all(checks)

def check_files():
    """Проверить необходимые файлы"""
    print("\n📁 Проверка файлов проекта...\n")
    
    required_files = [
        ".env",
        "bot.py",
        "config.py",
        "products.py",
        "faq.py",
        "gemini_handler.py",
        "requirements.txt",
    ]
    
    checks = []
    for filename in required_files:
        exists = Path(filename).exists()
        checks.append(print_status(f"Файл: {filename}", exists))
    
    # Проверить data.json (может не существовать изначально)
    data_json_exists = Path("data.json").exists()
    print_status("Файл: data.json (автосоздание)", True)  # Будет создан автоматически
    
    return all(checks)

def check_data():
    """Проверить базу данных"""
    print("\n💾 Проверка базы данных...\n")
    
    from products import CATEGORIES_DATA
    
    print(f"Найдено категорий: {len(CATEGORIES_DATA)}\n")
    
    for key, category in CATEGORIES_DATA.items():
        product_count = len(category.get("products", []))
        emoji = category.get("emoji", "?")
        name = category.get("name", "Unknown")
        print(f"   {emoji} {name}")
        print(f"      └─ Товаров: {product_count}")
    
    return True

def main():
    """Главная функция"""
    print("\n" + "="*50)
    print("🤖 ASMEBEL Bot - Test Script")
    print("="*50)
    
    all_ok = True
    
    # Проверить файлы
    try:
        all_ok = check_files() and all_ok
    except Exception as e:
        print(f"❌ Ошибка проверки файлов: {e}")
        all_ok = False
    
    # Проверить зависимости
    try:
        all_ok = check_dependencies() and all_ok
    except Exception as e:
        print(f"❌ Ошибка проверки зависимостей: {e}")
        all_ok = False
    
    # Проверить переменные окружения
    try:
        all_ok = check_environment() and all_ok
    except Exception as e:
        print(f"❌ Ошибка проверки окружения: {e}")
        all_ok = False
    
    # Проверить данные
    try:
        all_ok = check_data() and all_ok
    except Exception as e:
        print(f"❌ Ошибка проверки данных: {e}")
        all_ok = False
    
    # Итоговый результат
    print("\n" + "="*50)
    if all_ok:
        print("✅ ВСЕ ПРОВЕРКИ ПРОЙДЕНЫ!")
        print("\n🚀 Вы можете запустить бот командой:")
        print("   python bot.py")
        return 0
    else:
        print("❌ НЕКОТОРЫЕ ПРОВЕРКИ НЕ ПРОЙДЕНЫ!")
        print("\n📋 Проверьте выше какие файлы/зависимости отсутствуют")
        print("\n💡 Установка зависимостей:")
        print("   pip install -r requirements.txt")
        return 1
    
if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n❌ Прервано пользователем")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Непредвиденная ошибка: {e}")
        sys.exit(1)
