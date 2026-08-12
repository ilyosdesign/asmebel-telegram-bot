# bot.py - Render.com uchun optimiz qilingan

import logging
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

# Config
from config import TELEGRAM_TOKEN, ADMIN_ID, ADMIN_USERNAME
from gemini_handler import get_gemini_response
from products import CATEGORIES_DATA, add_product, delete_product, edit_product, add_category, delete_category
from faq import FAQ_DATA
from excel_handler import save_order_to_excel
from user_manager import add_user, get_all_user_ids

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ConversationHandler states
SELECT_CATEGORY, GET_PHOTO, GET_CAPTION = 0, 1, 2
DEL_SELECT_CAT, DEL_SELECT_PROD, DEL_CONFIRM = 3, 4, 5
EDIT_SELECT_CAT, EDIT_SELECT_PROD, EDIT_CHOOSE_FIELD, EDIT_GET_NEW_PHOTO, EDIT_GET_NEW_CAPTION = 6, 7, 8, 9, 10
MANAGE_CATS_MENU, ADD_CAT_GET_KEY, ADD_CAT_GET_NAME, ADD_CAT_GET_EMOJI, DEL_CAT_SELECT_FOR_DEL, DEL_CAT_CONFIRM_DEL = 11, 12, 13, 14, 15, 16
GET_PHONE_NUMBER = 17
GET_BROADCAST_MESSAGE, CONFIRM_BROADCAST = 18, 19

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if not update.message or not user:
        return

    add_user(user.id)

    await update.message.reply_html(
        f"Assalomu alaykum, {user.mention_html()}! Men <b>ASMEBEL</b> do'konining virtual yordamchisiman.\n\n"
        f"Menga mebellar haqida savol berishingiz yoki katalogimizni ko'rish uchun /katalog buyrug'ini yuborishingiz mumkin."
    )

# /katalog
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message and not update.callback_query:
        return

    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        button_text = f"{category['emoji']} {category['name']}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"cat_{key}")])

    if ADMIN_USERNAME:
        keyboard.append([InlineKeyboardButton("👨‍💼 Administrator bilan bog'lanish", url=f"https://t.me/{ADMIN_USERNAME}")])

    keyboard.append([InlineKeyboardButton("❓ Ko'p beriladigan savollar (FAQ)", callback_data='show_faq')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Asosiy kategoriyalardan birini tanlang:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)

# Button handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query or not query.data:
        return

    await query.answer()
    callback_data = query.data

    # Main menu
    if callback_data == 'main_menu':
        await show_catalog(update, context)

    # Categories
    elif callback_data.startswith('cat_'):
        category_key = callback_data.replace('cat_', '')
        if category_key in CATEGORIES_DATA:
            category = CATEGORIES_DATA[category_key]
            keyboard = []

            for product_key, product in category['products'].items():
                product_text = f"{product.get('emoji', '')} {product['name']}"
                keyboard.append([InlineKeyboardButton(product_text, callback_data=f"prod_{category_key}_{product_key}")])

            keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="main_menu")])
            reply_markup = InlineKeyboardMarkup(keyboard)

            await query.edit_message_text(
                f"<b>{category['emoji']} {category['name']}</b> kategoriyasidagi mahsulotlar:\n",
                reply_markup=reply_markup,
                parse_mode='HTML'
            )

    # Products
    elif callback_data.startswith('prod_'):
        parts = callback_data.replace('prod_', '').split('_')
        if len(parts) == 2:
            category_key, product_key = parts
            if category_key in CATEGORIES_DATA and product_key in CATEGORIES_DATA[category_key]['products']:
                product = CATEGORIES_DATA[category_key]['products'][product_key]

                keyboard = [
                    [InlineKeyboardButton("📞 Buyurtma qilish", callback_data=f"order_{category_key}_{product_key}")],
                    [InlineKeyboardButton("⬅️ Orqaga", callback_data=f"cat_{category_key}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                product_info = f"""
<b>{product.get('emoji', '')} {product['name']}</b>

📝 Tavsifi: {product.get('description', 'Tavsif mavjud emas')}
💰 Narxi: {product.get('price', 'Narx mavjud emas')}
"""

                if product.get('photo'):
                    await query.edit_message_caption(
                        caption=product_info,
                        reply_markup=reply_markup,
                        parse_mode='HTML'
                    )
                else:
                    await query.edit_message_text(
                        product_info,
                        reply_markup=reply_markup,
                        parse_mode='HTML'
                    )

    # FAQ
    elif callback_data == 'show_faq':
        keyboard = []
        for i, faq_item in enumerate(FAQ_DATA):
            keyboard.append([InlineKeyboardButton(f"❓ {faq_item['question']}", callback_data=f"faq_{i}")])
        keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data="main_menu")])
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.edit_message_text("Ko'p beriladigan savollar:", reply_markup=reply_markup)

    elif callback_data.startswith('faq_'):
        try:
            faq_index = int(callback_data.replace('faq_', ''))
            if 0 <= faq_index < len(FAQ_DATA):
                faq_item = FAQ_DATA[faq_index]
                keyboard = [
                    [InlineKeyboardButton("⬅️ Orqaga FAQ'ga", callback_data="show_faq")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.edit_message_text(
                    f"<b>❓ {faq_item['question']}</b>\n\n{faq_item['answer']}",
                    reply_markup=reply_markup,
                    parse_mode='HTML'
                )
        except (ValueError, IndexError):
            pass

# Error handler
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Exception while handling an update: {context.error}")

# Main
async def main() -> None:
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("katalog", show_catalog))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_error_handler(error_handler)

    logger.info("Bot starting...")

    # Render.com uchun: polling bilan ishga tushirish
    async with application:
        await application.start()
        logger.info("Bot is running!")
        await application.updater.start_polling(allowed_updates=Update.ALL_TYPES)
        logger.info("Polling started")

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
