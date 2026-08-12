# bot.py

import logging, asyncio
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters,
    ContextTypes, 
    CallbackQueryHandler,
    ConversationHandler
)
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.constants import ChatAction

# Mahalliy modullarni import qilish
from config import TELEGRAM_TOKEN, ADMIN_ID, ADMIN_USERNAME
from gemini_handler import get_gemini_response
from products import CATEGORIES_DATA, add_product, delete_product, edit_product, add_category, delete_category
from faq import FAQ_DATA
from excel_handler import save_order_to_excel
from user_manager import add_user, get_all_user_ids

# Loglashni sozlash (xatoliklarni oson topish uchun)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# ConversationHandler uchun holatlar (states)
# Mahsulot qo'shish holatlari
SELECT_CATEGORY, GET_PHOTO, GET_CAPTION = 0, 1, 2
# Mahsulot o'chirish holatlari
DEL_SELECT_CAT, DEL_SELECT_PROD, DEL_CONFIRM = 3, 4, 5
# Mahsulot tahrirlash holatlari
EDIT_SELECT_CAT, EDIT_SELECT_PROD, EDIT_CHOOSE_FIELD, EDIT_GET_NEW_PHOTO, EDIT_GET_NEW_CAPTION = 6, 7, 8, 9, 10
# Kategoriya boshqarish holatlari
MANAGE_CATS_MENU, ADD_CAT_GET_KEY, ADD_CAT_GET_NAME, ADD_CAT_GET_EMOJI, DEL_CAT_SELECT_FOR_DEL, DEL_CAT_CONFIRM_DEL = 11, 12, 13, 14, 15, 16
# Buyurtma berish holati
GET_PHONE_NUMBER = 17
# Ommaviy xabar yuborish holatlari
GET_BROADCAST_MESSAGE, CONFIRM_BROADCAST = 18, 19
 
# /start buyrug'iga javob beruvchi funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # Ob'ektlar None emasligini tekshirish
    if not update.message or not user:
        return

    # Foydalanuvchini bazaga qo'shish
    add_user(user.id)

    await update.message.reply_html(
        f"Assalomu alaykum, {user.mention_html()}! Men <b>ASMEBEL</b> do'konining virtual yordamchisiman.\n\n"
        f"Menga mebellar haqida savol berishingiz yoki katalogimizni ko'rish uchun /katalog buyrug'ini yuborishingiz mumkin."
    )

# /katalog buyrug'i uchun funksiya
async def show_catalog(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Katalog kategoriyalarini tugmalar bilan ko'rsatadi."""
    # Ob'ekt None emasligini tekshirish
    if not update.message and not update.callback_query:
        return

    # Kategoriyalar ro'yxatidan dinamik ravishda tugmalar yaratish
    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        button_text = f"{category['emoji']} {category['name']}"
        keyboard.append([InlineKeyboardButton(button_text, callback_data=f"cat_{key}")])

    # Administrator bilan bog'lanish tugmasini qo'shish
    if ADMIN_USERNAME:
        keyboard.append([InlineKeyboardButton("👨‍💼 Administrator bilan bog'lanish", url=f"https://t.me/{ADMIN_USERNAME}")])

    keyboard.append([InlineKeyboardButton("❓ Ko'p beriladigan savollar (FAQ)", callback_data='show_faq')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "Asosiy kategoriyalardan birini tanlang:"

    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup)
    elif update.message:
        await update.message.reply_text(text, reply_markup=reply_markup)

# Tugmalar bosilganda ishlaydigan funksiya
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tugmalar bosilganda javob qaytaradi."""
    query = update.callback_query
    # Ob'ektlar None emasligini tekshirish
    if not query or not query.data: 
        return
    await query.answer()  # Tugma bosilganini tasdiqlash

    callback_data = query.data

    # Asosiy menyuga qaytish
    if callback_data == 'main_menu':
        await show_catalog(update, context)
        return

    # FAQ bo'limini ko'rsatish
    if callback_data == 'show_faq':
        await show_faq(update, context)
        return
    
    # FAQ savoliga javob berish
    elif callback_data.startswith('faq_q_'):
        await show_faq_answer(update, context)
        return

    # Kategoriya tanlanganda (mahsulotlar ro'yxatini ko'rsatish)
    if callback_data.startswith('cat_'):
        category_key = callback_data.split('_', 1)[1]
        category = CATEGORIES_DATA.get(category_key)
        
        if category:
            products = category.get('products', [])
            keyboard = []
            if not products:
                text = (
                    f"<b>{category['name']}</b> bo'limida hozircha mahsulotlar yo'q.\n\n"
                    "Tez orada yangi mebellar qo'shiladi."
                )
            else:
                text = f"<b>{category['name']}</b> bo'limidagi mahsulotlar:"
                for product in products:
                    # Tavsif bo'lmasa, xatolikni oldini olish
                    product_name = product.get('caption', 'Nomsiz mahsulot').split('\n')[0]
                    keyboard.append([InlineKeyboardButton(
                        product_name, 
                        callback_data=f"prod_{category_key}_{product['id']}"
                    )])
            
            keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data='main_menu')])
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text(text=text, reply_markup=reply_markup, parse_mode="HTML")

    # Mahsulot tanlanganda (rasm va tavsifni ko'rsatish)
    elif callback_data.startswith('prod_'):
        parts = callback_data.split('_', 2)
        if len(parts) != 3:
            await query.answer("Xatolik: Mahsulot topilmadi.", show_alert=True)
            return
        _, category_key, product_id_str = parts
        try:
            product_id = int(product_id_str)
            
            category = CATEGORIES_DATA.get(category_key)
            product_to_show = None
            if category:
                for p in category.get('products', []):
                    if p.get('id') == product_id:
                        product_to_show = p
                        break
            
            if product_to_show:
                keyboard = [
                    [InlineKeyboardButton("🛒 Buyurtma berish", callback_data=f"order_{category_key}_{product_id}")],
                    [InlineKeyboardButton("⬅️ Orqaga (Mahsulotlar ro'yxati)", callback_data=f"cat_{category_key}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                # Oldingi matnli xabarni o'chirib, rasm yuboramiz
                if query.message:
                    await query.delete_message()
                
                if not update.effective_chat:
                    await query.answer("Xatolik: Chat topilmadi.", show_alert=True)
                    return

                try:
                    logger.info(f"Rasm jo'natishga urinish: chat_id={update.effective_chat.id}, photo_id={product_to_show.get('photo_id')}")
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=product_to_show['photo_id'],
                        caption=product_to_show['caption'],
                        reply_markup=reply_markup,
                        parse_mode="HTML" # Tavsifda HTML ishlatish uchun
                    )
                except Exception as e:
                    logger.error(f"RASM YUBORISHDA XATOLIK YUZ BERDI: {e}")
                    await query.answer("Kechirasiz, rasm yuklashda xatolik yuz berdi.", show_alert=True)
            else:
                await query.answer("Kechirasiz, bu mahsulot topilmadi.", show_alert=True)
        except Exception as e:
            logger.error(f"Mahsulotni ko'rsatishda umumiy xatolik: {e}")
            await query.answer("Noma'lum xatolik yuz berdi.", show_alert=True)

# Matnli xabarlarni Gemini'ga yuboruvchi funksiya
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Ob'ektlar None emasligini tekshirish
    if not update.message or not update.message.text or not update.effective_chat:
        return

    user_message = update.message.text
    
    # Foydalanuvchiga "yozayapman..." holatini ko'rsatish
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action=ChatAction.TYPING)

    # Gemini'dan javob olish
    response_text = await get_gemini_response(user_message)
    
    # Foydalanuvchiga javob yuborish
    await update.message.reply_text(response_text)

# --- FAQ Functions ---

async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """FAQ savollari ro'yxatini ko'rsatadi."""
    query = update.callback_query
    if query:
        await query.answer()

    keyboard = []
    for item in FAQ_DATA:
        keyboard.append([InlineKeyboardButton(item['question'], callback_data=f"faq_q_{item['id']}")])
    
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga (Katalog)", callback_data='main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    text = "<b>Ko'p beriladigan savollar:</b>"
    if query:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

async def show_faq_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Tanlangan FAQ savoliga javobni ko'rsatadi."""
    query = update.callback_query
    if not query or not query.data:
        return
    await query.answer()

    question_id = query.data.split('faq_q_')[1]
    answer_item = next((item for item in FAQ_DATA if item['id'] == question_id), None)

    if answer_item:
        text = answer_item['answer']
        keyboard = [[InlineKeyboardButton("⬅️ Orqaga (Savollar)", callback_data='show_faq')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode="HTML")

# --- Admin Panel Conversation ---

# Admin uchun buyruq
async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    # Foydalanuvchi admin ekanligini tekshirish
    if not update.message or not user or (ADMIN_ID and str(user.id) != ADMIN_ID):
        if update.message:
            await update.message.reply_text("Kechirasiz, sizda bu buyruqdan foydalanish uchun ruxsat yo'q.")
        return

    keyboard = [
        [InlineKeyboardButton("➕ Mahsulot qo'shish", callback_data='add_product')],
        [InlineKeyboardButton("✏️ Mahsulotni tahrirlash", callback_data='edit_product')],
        [InlineKeyboardButton("🗑️ Mahsulotni o'chirish", callback_data='delete_product')],
        [InlineKeyboardButton("🗂️ Kategoriyalarni boshqarish", callback_data='manage_categories')],
        [InlineKeyboardButton("📢 Xabar yuborish", callback_data='broadcast_start')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Salom, Admin! Boshqaruv panelidasiz.", reply_markup=reply_markup)

async def add_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Mahsulot qo'shish jarayonini boshlaydi, kategoriya tanlashni so'raydi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        keyboard.append([InlineKeyboardButton(category['name'], callback_data=f"add_cat_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Mahsulotni qaysi kategoriyaga qo'shmoqchisiz? (/cancel - bekor qilish)",
        reply_markup=reply_markup
    )
    return SELECT_CATEGORY

async def select_category_for_add(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kategoriyani saqlaydi va rasm yuborishni so'raydi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END

    await query.answer()
    category_key = query.data.replace("add_cat_", "")

    context.user_data['category_key'] = category_key
    await query.edit_message_text(text="Ajoyib! Endi mahsulot rasmini yuboring. (/cancel - bekor qilish)")

    return GET_PHOTO

async def get_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Rasmni saqlaydi va tavsif (caption) kiritishni so'raydi."""
    if not update.message:
        return GET_PHOTO
    
    # Agar rasm yubormasa
    if not update.message.photo:
        await update.message.reply_text("❌ Iltimos, faqat rasm yuboring. (/cancel - bekor qilish)\n\n💡 Rasm sifatida: PNG, JPG, GIF, WebP")
        return GET_PHOTO
    
    if not context.user_data:
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos /admin buyrug'ini qayta yuboring.")
        return ConversationHandler.END

    try:
        photo_id = update.message.photo[-1].file_id
        context.user_data['photo_id'] = photo_id
        logger.info(f"📸 Rasm saqlandi. Photo ID: {photo_id[:20]}...")
    except Exception as e:
        logger.error(f"❌ Rasm olinishda xatolik: {e}")
        await update.message.reply_text("❌ Rasm olinishda xatolik yuz berdi. Qayta harakat qiling.")
        return GET_PHOTO
    
    await update.message.reply_text(
        "✅ Rasm qabul qilindi!\n\n"
        "Endi mahsulot nomini va tavsifini yuboring. (/cancel - bekor qilish)\n\n"
        "<b>📝 Namuna:</b>\n\n"
        "<b>Yangi Divan</b>\n"
        "Narxi: 3,000,000 so'm\n"
        "Material: XDF",
        parse_mode="HTML"
    )
    return GET_CAPTION

async def get_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tavsifni saqlaydi, mahsulotni qo'shadi va jarayonni yakunlaydi."""
    if not update.message:
        return GET_CAPTION
    
    if not update.message.text:
        await update.message.reply_text("❌ Iltimos, matn kiriting. (/cancel - bekor qilish)")
        return GET_CAPTION
    
    if not context.user_data:
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos /admin buyrug'ini qayta yuboring.")
        return ConversationHandler.END

    caption = update.message.text
    category_key = context.user_data.get('category_key')
    photo_id = context.user_data.get('photo_id')
    
    if category_key and photo_id:
        try:
            add_product(category_key, photo_id, caption)
            logger.info(f"✅ Mahsulot qo'shildi: {category_key} - {caption[:30]}...")
            await update.message.reply_text("✅ Mahsulot muvaffaqiyatli qo'shildi!")
        except Exception as e:
            logger.error(f"❌ Mahsulot qo'shishda xatolik: {e}")
            await update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")
    else:
        await update.message.reply_text("❌ Xatolik yuz berdi. Kerakli ma'lumotlar topilmadi. Jarayon bekor qilindi.")
        logger.error(f"❌ category_key yoki photo_id yo'q: category={category_key}, photo={photo_id is not None}")
    
    context.user_data.clear()
    return ConversationHandler.END

# --- Mahsulot o'chirish jarayoni ---

async def delete_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Mahsulot o'chirish jarayonini boshlaydi, kategoriya tanlashni so'raydi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        keyboard.append([InlineKeyboardButton(category['name'], callback_data=f"del_cat_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Qaysi kategoriyadagi mahsulotni o'chirmoqchisiz? (/cancel - bekor qilish)",
        reply_markup=reply_markup
    )
    return DEL_SELECT_CAT

async def delete_category_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kategoriyani saqlaydi va o'chirish uchun mahsulotlar ro'yxatini ko'rsatadi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    category_key = query.data.replace("del_cat_", "")
    context.user_data['del_category_key'] = category_key
    
    category = CATEGORIES_DATA.get(category_key)
    if not category:
        await query.edit_message_text(text="Xato: Kategoriya topilmadi.")
        if context.user_data:
            context.user_data.clear()
        return ConversationHandler.END
    products = category.get('products', [])
    
    if not products:
        await query.edit_message_text(text="Bu kategoriyada mahsulotlar yo'q.")
        context.user_data.clear()
        return ConversationHandler.END

    keyboard = []
    for product in products:
        product_name = product.get('caption', 'Nomsiz mahsulot').split('\n')[0]
        keyboard.append([InlineKeyboardButton(product_name, callback_data=str(product['id']))])
    
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data='back_to_del_cat_select')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="O'chirish uchun mahsulotni tanlang:",
        reply_markup=reply_markup
    )
    return DEL_SELECT_PROD

async def delete_product_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Mahsulotni saqlaydi va o'chirishni tasdiqlashni so'raydi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    
    if query.data == 'back_to_del_cat_select':
        # Bu funksiya endi delete_product_start orqali chaqiriladi
        # Shunchaki suhbatni to'g'ri holatga qaytaramiz
        if query:
            await query.answer()
        await delete_product_start(update, context)
        return DEL_SELECT_CAT

    product_id = int(query.data)
    context.user_data['del_product_id'] = product_id
    
    category_key = context.user_data.get('del_category_key')
    if not category_key:
        await query.edit_message_text("Xatolik: Kategoriya kaliti topilmadi.")
        context.user_data.clear()
        return ConversationHandler.END

    category = CATEGORIES_DATA.get(category_key)
    if not category:
        await query.edit_message_text("Xatolik: Kategoriya topilmadi.")
        context.user_data.clear()
        return ConversationHandler.END

    product = next((p for p in category.get('products', []) if p.get('id') == product_id), None)
    
    if not product:
        await query.edit_message_text("Xatolik: Mahsulot topilmadi.")
        context.user_data.clear()
        return ConversationHandler.END
        
    product_name = product.get('caption', 'Nomsiz mahsulot').split('\n')[0]
    
    keyboard = [[
        InlineKeyboardButton("✅ Ha", callback_data='confirm_delete'),
        InlineKeyboardButton("❌ Yo'q", callback_data='cancel_delete')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Haqiqatdan ham <b>{product_name}</b> mahsulotini o'chirmoqchimisiz?",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    return DEL_CONFIRM

async def delete_product_confirm(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tasdiqlansa, mahsulotni o'chiradi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    
    if query.data == 'confirm_delete' and context.user_data.get('del_category_key') and context.user_data.get('del_product_id'):
        delete_product(context.user_data['del_category_key'], context.user_data['del_product_id'])
        await query.edit_message_text("🗑️ Mahsulot muvaffaqiyatli o'chirildi.")
    else:
        await query.edit_message_text("Amal bekor qilindi.")
        
    context.user_data.clear()
    return ConversationHandler.END

# --- Mahsulot tahrirlash jarayoni ---

async def edit_product_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tahrirlash uchun kategoriya tanlashni so'raydi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        keyboard.append([InlineKeyboardButton(category['name'], callback_data=f"edit_cat_{key}")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Qaysi kategoriyadagi mahsulotni tahrirlamoqchisiz? (/cancel - bekor qilish)",
        reply_markup=reply_markup
    )
    return EDIT_SELECT_CAT

async def edit_category_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tahrirlash uchun mahsulotlar ro'yxatini ko'rsatadi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    category_key = query.data.replace("edit_cat_", "")
    context.user_data['edit_category_key'] = category_key
    
    products = CATEGORIES_DATA.get(category_key, {}).get('products', [])
    
    if not products:
        await query.edit_message_text(text="Bu kategoriyada mahsulotlar yo'q.")
        context.user_data.clear()
        return ConversationHandler.END

    keyboard = [[InlineKeyboardButton(p.get('caption', 'Nomsiz mahsulot').split('\n')[0], callback_data=str(p['id']))] for p in products]
    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data='back_to_edit_cat_select')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Tahrirlash uchun mahsulotni tanlang:", reply_markup=reply_markup)
    return EDIT_SELECT_PROD

async def edit_product_select(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nimani tahrirlashni so'raydi (rasm yoki tavsif)."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()

    if query.data == 'back_to_edit_cat_select':
        # Bu funksiya endi edit_product_start orqali chaqiriladi
        # Shunchaki suhbatni to'g'ri holatga qaytaramiz
        if query:
            await query.answer()
        await edit_product_start(update, context)
        return EDIT_SELECT_CAT

    context.user_data['edit_product_id'] = int(query.data)
    
    keyboard = [
        [InlineKeyboardButton("🖼️ Rasmni o'zgartirish", callback_data='edit_photo')],
        [InlineKeyboardButton("📝 Tavsifni o'zgartirish", callback_data='edit_caption')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(text="Nimani o'zgartirmoqchisiz?", reply_markup=reply_markup)
    return EDIT_CHOOSE_FIELD

async def edit_choose_field(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tanlangan maydon uchun yangi ma'lumotni so'raydi."""
    query = update.callback_query
    if not query or not query.data:
        return ConversationHandler.END
    await query.answer()
    
    if query.data == 'edit_photo':
        await query.edit_message_text("Yangi rasmni yuboring. (/cancel - bekor qilish)")
        return EDIT_GET_NEW_PHOTO
    elif query.data == 'edit_caption':
        await query.edit_message_text(
            "Yangi nom va tavsifni yuboring. (/cancel - bekor qilish)\n\n"
            "<b>Eslatma:</b> Eski tavsif to'liq o'chib, o'rniga yangisi yoziladi.",
            parse_mode="HTML"
        )
        return EDIT_GET_NEW_CAPTION
    return ConversationHandler.END

async def edit_get_new_photo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi rasmni saqlaydi va mahsulotni yangilaydi."""
    if not update.message:
        return EDIT_GET_NEW_PHOTO
    
    if not update.message.photo:
        await update.message.reply_text("❌ Iltimos, faqat rasm yuboring. (/cancel - bekor qilish)")
        return EDIT_GET_NEW_PHOTO
    
    if not context.user_data:
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos /admin buyrug'ini qayta yuboring.")
        return ConversationHandler.END

    category_key = context.user_data.get('edit_category_key')
    product_id = context.user_data.get('edit_product_id')
    
    try:
        new_photo_id = update.message.photo[-1].file_id

        if category_key and product_id:
            edit_product(category_key, product_id, {'photo_id': new_photo_id})
            logger.info(f"✅ Rasm yangilandi: {category_key} - product_id={product_id}")
            await update.message.reply_text("✅ Rasm muvaffaqiyatli yangilandi!")
        else:
            await update.message.reply_text("❌ Xatolik yuz berdi. Kerakli ma'lumotlar topilmadi.")
            logger.error(f"❌ category_key yoki product_id yo'q: cat={category_key}, prod={product_id}")
    except Exception as e:
        logger.error(f"❌ Rasmni yangilashda xatolik: {e}")
        await update.message.reply_text(f"❌ Xatolik yuz berdi: {str(e)}")

    context.user_data.clear()
    return ConversationHandler.END

async def edit_get_new_caption(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi tavsifni saqlaydi va mahsulotni yangilaydi."""
    if not update.message:
        return EDIT_GET_NEW_CAPTION
    if not update.message.text or not context.user_data:
        await update.message.reply_text("Iltimos, matn kiriting. (/cancel - bekor qilish)")
        return EDIT_GET_NEW_CAPTION

    category_key = context.user_data.get('edit_category_key')
    product_id = context.user_data.get('edit_product_id')
    new_caption = update.message.text

    if category_key and product_id:
        edit_product(category_key, product_id, {'caption': new_caption})
        await update.message.reply_text("✅ Tavsif muvaffaqiyatli yangilandi!")
    else:
        await update.message.reply_text("❌ Xatolik yuz berdi.")

    context.user_data.clear()
    return ConversationHandler.END

# --- Kategoriya boshqarish jarayoni ---

async def manage_categories_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kategoriyalarni boshqarish menyusini ko'rsatadi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    keyboard = [
        [InlineKeyboardButton("➕ Yangi kategoriya qo'shish", callback_data='cat_add_start')],
        [InlineKeyboardButton("➖ Kategoriyani o'chirish", callback_data='cat_del_start')],
        [InlineKeyboardButton("⬅️ Orqaga", callback_data='back_to_admin_panel')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Kategoriyalarni boshqarish bo'limi:",
        reply_markup=reply_markup
    )
    return MANAGE_CATS_MENU

async def back_to_admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Suhbatni tugatadi va admin paneliga qaytishni taklif qiladi."""
    query = update.callback_query
    if not query or not query.message:
        return ConversationHandler.END
    await query.answer()
    # Asosiy admin panelini qayta ko'rsatish
    keyboard = [
        [InlineKeyboardButton("➕ Mahsulot qo'shish", callback_data='add_product')],
        [InlineKeyboardButton("✏️ Mahsulotni tahrirlash", callback_data='edit_product')],
        [InlineKeyboardButton("🗑️ Mahsulotni o'chirish", callback_data='delete_product')],
        [InlineKeyboardButton("🗂️ Kategoriyalarni boshqarish", callback_data='manage_categories')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text("Salom, Admin! Boshqaruv panelidasiz.", reply_markup=reply_markup)
    # Suhbatni tugatmasdan, admin panelining o'ziga qaytaramiz
    return ConversationHandler.END # Bu suhbatni tugatadi, lekin yangisini boshlashga imkon beradi.

async def add_category_start_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yangi kategoriya uchun unikal kalit so'raydi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()
    await query.edit_message_text(
        "Yangi kategoriya uchun unikal kalit so'z kiriting (masalan: `yangi_mebel`).\n"
        "Faqat lotin harflari, raqamlar va pastki chiziq. (/cancel - bekor qilish)",
        parse_mode="Markdown"
    )
    return ADD_CAT_GET_KEY

async def add_category_get_key(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kalitni oladi, tekshiradi va nomini so'raydi."""
    if not update.message or not update.message.text or not context.user_data:
        return ADD_CAT_GET_KEY
    category_key = update.message.text.strip().lower()
    
    if " " in category_key or not category_key.isascii() or not category_key:
        await update.message.reply_text("Xato: Kalit bo'sh bo'lishi, bo'shliq yoki lotin bo'lmagan belgilar bo'lmasligi kerak. Qayta kiriting.")
        return ADD_CAT_GET_KEY
    if category_key in CATEGORIES_DATA:
        await update.message.reply_text("Bu kalit so'z allaqachon mavjud. Boshqa kalit kiriting.")
        return ADD_CAT_GET_KEY
        
    context.user_data['new_cat_key'] = category_key
    await update.message.reply_text("Ajoyib! Endi kategoriya nomini kiriting (masalan: 'Yangi Mebellar').")
    return ADD_CAT_GET_NAME

async def add_category_get_name(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Nomni oladi va emoji so'raydi."""
    if not update.message or not update.message.text or not context.user_data:
        return ADD_CAT_GET_NAME
    context.user_data['new_cat_name'] = update.message.text.strip()
    await update.message.reply_text("Yaxshi! Endi kategoriya uchun emoji kiriting (masalan: ✨).")
    return ADD_CAT_GET_EMOJI

async def add_category_get_emoji(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Emojini oladi, kategoriyani qo'shadi va tugatadi."""
    if not update.message or not update.message.text or not context.user_data:
        return ADD_CAT_GET_EMOJI
    emoji = update.message.text.strip()

    key = context.user_data.get('new_cat_key')
    name = context.user_data.get('new_cat_name')
    
    if not key or not name:
        await update.message.reply_text("❌ Xatolik yuz berdi. Jarayon bekor qilindi.")
        context.user_data.clear()
        return ConversationHandler.END

    add_category(key, name, emoji)
    await update.message.reply_text(f"✅ '{name}' kategoriyasi muvaffaqiyatli qo'shildi!")
    context.user_data.clear()
    return ConversationHandler.END

async def delete_category_start_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """O'chirish uchun kategoriyalar ro'yxatini ko'rsatadi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()

    keyboard = []
    for key, category in CATEGORIES_DATA.items():
        product_count = len(category.get('products', []))
        button_text = f"{category['name']} ({product_count} mahsulot)"
        # Faqat bo'sh kategoriyalarni o'chirishga ruxsat beramiz
        if product_count == 0:
            keyboard.append([InlineKeyboardButton(button_text, callback_data=key)])
    
    if not keyboard:
        await query.edit_message_text("O'chirish uchun mos (bo'sh) kategoriyalar topilmadi.")
        return ConversationHandler.END

    keyboard.append([InlineKeyboardButton("⬅️ Orqaga", callback_data='back_to_manage_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="O'chirish uchun kategoriyani tanlang.\n"
             "Eslatma: Faqat ichida mahsuloti yo'q kategoriyalarni o'chirish mumkin.",
        reply_markup=reply_markup
    )
    return DEL_CAT_SELECT_FOR_DEL

async def back_to_manage_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kategoriyalarni boshqarish menyusiga qaytadi."""
    await manage_categories_start(update, context)
    return MANAGE_CATS_MENU

async def delete_category_select_for_del(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tanlangan kategoriyani o'chirishni tasdiqlashni so'raydi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    category_key = query.data
    context.user_data['del_cat_key'] = category_key

    if category_key not in CATEGORIES_DATA:
        await query.edit_message_text("Xato: Kategoriya topilmadi.")
        context.user_data.clear()
        return ConversationHandler.END
    category_name = CATEGORIES_DATA[category_key]['name']
    
    keyboard = [[
        InlineKeyboardButton("✅ Ha, o'chirish", callback_data='confirm_del_cat'),
        InlineKeyboardButton("❌ Yo'q", callback_data='cancel_del_cat')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text=f"Haqiqatdan ham <b>{category_name}</b> kategoriyasini o'chirmoqchimisiz?",
        reply_markup=reply_markup, parse_mode="HTML"
    )
    return DEL_CAT_CONFIRM_DEL

async def delete_category_confirm_del(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Kategoriyani o'chiradi va tugatadi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()
    if query.data == 'confirm_del_cat' and context.user_data.get('del_cat_key'):
        delete_category(context.user_data['del_cat_key'])
        await query.edit_message_text("🗑️ Kategoriya muvaffaqiyatli o'chirildi.")
    else:
        await query.edit_message_text("Amal bekor qilindi.")
    context.user_data.clear()
    return ConversationHandler.END

# --- Buyurtma berish jarayoni ---

async def order_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Buyurtma berish jarayonini boshlaydi, telefon raqam so'raydi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data or not update.effective_chat:
        return ConversationHandler.END
    await query.answer()

    # Mahsulot ma'lumotlarini saqlab qo'yish
    context.user_data['order_callback'] = query.data

    # Telefon raqamni so'rash uchun ReplyKeyboardMarkup
    keyboard = [
        [KeyboardButton("📞 Telefon raqamni yuborish", request_contact=True)]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)

    # Oldingi inline tugmalarni o'chirish
    if query.message:
        await query.edit_message_reply_markup(reply_markup=None) 

    # Yangi xabar yuborish
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Buyurtmani tasdiqlash uchun, iltimos, telefon raqamingizni yuboring.",
        reply_markup=reply_markup
    )
    return GET_PHONE_NUMBER

async def get_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Telefon raqamni oladi va adminga yuboradi."""
    if not update.message or not update.message.contact or not context.user_data or not update.effective_user:
        if update.message: await update.message.reply_text("Iltimos, tugma orqali raqamingizni yuboring.")
        return GET_PHONE_NUMBER

    contact = update.message.contact
    phone_number = contact.phone_number
    user = update.effective_user

    callback_data = context.user_data.get('order_callback')
    if not callback_data:
        await update.message.reply_text("❌ Xatolik yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        return ConversationHandler.END

    _, category_key, product_id_str = callback_data.split('_', 2)
    product_id = int(product_id_str)
    category = CATEGORIES_DATA.get(category_key)
    if not category:
        await update.message.reply_text("❌ Xatolik: Kategoriya topilmadi.", reply_markup=ReplyKeyboardRemove())
        return ConversationHandler.END

    product = next((p for p in category['products'] if p['id'] == product_id), None)

    if product and ADMIN_ID:
        product_name = product.get('caption', 'Nomsiz mahsulot').split('\n')[0]
        
        admin_message = (
            f"📢 <b>Yangi buyurtma!</b>\n\n"
            f"<b>Mahsulot:</b> {product_name}\n"
            f"<b>Mijoz:</b> {user.mention_html()}\n"
            f"<b>ID:</b> <code>{user.id}</code>\n"
            f"<b>Telefon:</b> <code>{phone_number}</code>"
        )
        await context.bot.send_message(chat_id=int(ADMIN_ID), text=admin_message, parse_mode="HTML")

        # Excelga saqlash
        user_info = {'id': user.id, 'username': user.username, 'full_name': user.full_name, 'phone_number': phone_number}
        save_order_to_excel(user_info, product_name)
        
        await update.message.reply_text(
            "✅ Buyurtmangiz qabul qilindi. Tez orada administrator siz bilan bog'lanadi!",
            reply_markup=ReplyKeyboardRemove() # Klaviaturani olib tashlash
        )
    else:
        await update.message.reply_text("❌ Xatolik: Mahsulot topilmadi yoki admin sozlanmagan.", reply_markup=ReplyKeyboardRemove())

    context.user_data.clear()
    return ConversationHandler.END

# --- Ommaviy xabar yuborish (Broadcast) ---

async def broadcast_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ommaviy xabar yuborish jarayonini boshlaydi."""
    query = update.callback_query
    if not query:
        return ConversationHandler.END
    await query.answer()
    await query.edit_message_text(
        "Foydalanuvchilarga yuborish uchun xabar matnini kiriting. Rasm bilan yuborish ham mumkin.\n\n"
        "Bekor qilish uchun /cancel buyrug'ini yuboring."
    )
    return GET_BROADCAST_MESSAGE

async def get_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Yuboriladigan xabarni oladi va tasdiqlashni so'raydi."""
    if not update.message or not context.user_data:
        return GET_BROADCAST_MESSAGE

    context.user_data['broadcast_message'] = update.message
    user_count = len(get_all_user_ids())

    keyboard = [
        [InlineKeyboardButton("✅ Ha, yuborish", callback_data='confirm_broadcast')],
        [InlineKeyboardButton("❌ Yo'q, bekor qilish", callback_data='cancel_broadcast')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        f"Ushbu xabar {user_count} ta foydalanuvchiga yuboriladi. Tasdiqlaysizmi?",
        reply_markup=reply_markup
    )
    return CONFIRM_BROADCAST

async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Tasdiqlanganda xabarni barcha foydalanuvchilarga yuboradi."""
    query = update.callback_query
    if not query or not query.data or not context.user_data:
        return ConversationHandler.END
    await query.answer()

    if query.data == 'cancel_broadcast':
        await query.edit_message_text("Xabar yuborish bekor qilindi.")
        context.user_data.clear()
        return ConversationHandler.END

    message_to_send = context.user_data.get('broadcast_message')
    if not message_to_send:
        await query.edit_message_text("Xatolik: Yuboriladigan xabar topilmadi.")
        return ConversationHandler.END

    await query.edit_message_text("Xabar yuborish boshlandi... Bu biroz vaqt olishi mumkin.")
    
    user_ids = get_all_user_ids()
    sent_count = 0
    for user_id in user_ids:
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=message_to_send.chat_id, message_id=message_to_send.message_id)
            sent_count += 1
            await asyncio.sleep(0.1) # Telegram limitlariga tushmaslik uchun
        except Exception as e:
            logger.warning(f"Foydalanuvchi {user_id} ga xabar yuborib bo'lmadi: {e}")

    await query.message.reply_text(f"✅ Xabar yuborish yakunlandi!\n\n{sent_count} ta foydalanuvchiga muvaffaqiyatli yuborildi.")
    context.user_data.clear()
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Joriy suhbatni bekor qiladi."""
    message = update.message
    if update.callback_query and update.callback_query.message:
        await update.callback_query.edit_message_text("Amal bekor qilindi.")
    elif message:
        await message.reply_text("Amal bekor qilindi.")
    if context.user_data:
        context.user_data.clear()
    return ConversationHandler.END

async def cancel_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Buyurtma suhbatini bekor qiladi."""
    query = update.callback_query
    if query:
        await query.answer()
        # Agar xabar matnli bo'lsa, uni tahrirlaymiz
        if query.message and hasattr(query.message, "text") and query.message.text:
            await query.edit_message_text("Buyurtma bekor qilindi.")
        elif update.effective_chat:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Buyurtma bekor qilindi.", reply_markup=ReplyKeyboardRemove())
    if context.user_data:
        context.user_data.clear()
    return ConversationHandler.END

def main() -> None:
    """Botni ishga tushirish."""
    if not TELEGRAM_TOKEN:
        logger.error(".env faylida TELEGRAM_TOKEN topilmadi yoki bo'sh.")
        return
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # Mahsulot qo'shish uchun ConversationHandler
    add_product_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(add_product_start, pattern='^add_product$')],
        states={
            SELECT_CATEGORY: [CallbackQueryHandler(select_category_for_add, pattern=f"^add_cat_({'|'.join(CATEGORIES_DATA.keys())})$")],
            GET_PHOTO: [MessageHandler(filters.PHOTO, get_photo)],
            GET_CAPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_caption)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )

    # Mahsulot o'chirish uchun ConversationHandler
    delete_product_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(delete_product_start, pattern='^delete_product$')],
        states={
            DEL_SELECT_CAT: [CallbackQueryHandler(delete_category_select, pattern=f"^del_cat_({'|'.join(CATEGORIES_DATA.keys())})$")],
            DEL_SELECT_PROD: [CallbackQueryHandler(delete_product_select, pattern=r'^\d+$|^back_to_del_cat_select$')],
            DEL_CONFIRM: [CallbackQueryHandler(delete_product_confirm, pattern='^(confirm_delete|cancel_delete)$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )

    # Mahsulot tahrirlash uchun ConversationHandler
    edit_product_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(edit_product_start, pattern='^edit_product$')],
        states={
            EDIT_SELECT_CAT: [CallbackQueryHandler(edit_category_select, pattern=f"^edit_cat_({'|'.join(CATEGORIES_DATA.keys())})$")],
            EDIT_SELECT_PROD: [CallbackQueryHandler(edit_product_select, pattern=r'^\d+$|^back_to_edit_cat_select$')],
            EDIT_CHOOSE_FIELD: [CallbackQueryHandler(edit_choose_field, pattern='^(edit_photo|edit_caption)$')],
            EDIT_GET_NEW_PHOTO: [MessageHandler(filters.PHOTO, edit_get_new_photo)],
            EDIT_GET_NEW_CAPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_get_new_caption)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )

    # Kategoriya boshqarish uchun ConversationHandler
    manage_cats_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(manage_categories_start, pattern='^manage_categories$')],
        states={
            MANAGE_CATS_MENU: [
                CallbackQueryHandler(add_category_start_prompt, pattern='^cat_add_start$'),
                CallbackQueryHandler(delete_category_start_prompt, pattern='^cat_del_start$'),
                CallbackQueryHandler(back_to_admin_panel, pattern='^back_to_admin_panel$')
            ],
            ADD_CAT_GET_KEY: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_category_get_key)],
            ADD_CAT_GET_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_category_get_name)],
            ADD_CAT_GET_EMOJI: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_category_get_emoji)],
            DEL_CAT_SELECT_FOR_DEL: [
                CallbackQueryHandler(back_to_manage_menu, pattern='^back_to_manage_menu$'),
                CallbackQueryHandler(delete_category_select_for_del, pattern=f"^({'|'.join(CATEGORIES_DATA.keys())})$") # Catches specific category keys
            ],
            DEL_CAT_CONFIRM_DEL: [CallbackQueryHandler(delete_category_confirm_del, pattern='^(confirm_del_cat|cancel_del_cat)$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )

    # Buyurtma berish uchun ConversationHandler
    order_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(order_start, pattern='^order_')],
        states={
            GET_PHONE_NUMBER: [MessageHandler(filters.CONTACT, get_phone_number)],
        },
        fallbacks=[CallbackQueryHandler(cancel_order, pattern='^cancel_order$'), CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )

    # Ommaviy xabar yuborish uchun ConversationHandler
    broadcast_conv = ConversationHandler(
        entry_points=[CallbackQueryHandler(broadcast_start, pattern='^broadcast_start$')],
        states={
            GET_BROADCAST_MESSAGE: [MessageHandler(filters.ALL & ~filters.COMMAND, get_broadcast_message)],
            CONFIRM_BROADCAST: [CallbackQueryHandler(confirm_broadcast, pattern='^(confirm_broadcast|cancel_broadcast)$')],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
        per_user=True,
        per_chat=True,
    )
    # Buyruq va xabarlarni qayd etish
    application.add_handler(add_product_conv)
    application.add_handler(delete_product_conv)
    application.add_handler(edit_product_conv)
    application.add_handler(manage_cats_conv)
    application.add_handler(order_conv)
    application.add_handler(broadcast_conv)
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("katalog", show_catalog))
    application.add_handler(CommandHandler("admin", admin_panel))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    # Muhim: Umumiy CallbackQueryHandler boshqa handlerlardan keyin turishi kerak
    application.add_handler(CallbackQueryHandler(button_handler))

    # Botni ishga tushirish
    print("Bot ishga tushdi...")
    application.run_polling()

if __name__ == '__main__':
    main()
