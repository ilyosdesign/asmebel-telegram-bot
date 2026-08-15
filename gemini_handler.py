# gemini_handler.py

import logging
import asyncio
from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from config import GEMINI_API_KEY
from products import get_categories_for_prompt

logger = logging.getLogger(__name__)

try:
    configure(api_key=GEMINI_API_KEY)
    model = GenerativeModel(model_name="gemini-1.5-pro-latest")
    categories_prompt = get_categories_for_prompt()

    chat = model.start_chat(history=[
        {
            "role": "user",
            "parts": [f"""Sen "ASMEBEL" online do'konining virtual yordamchisisan.
Sening vazifang - mijozlarga xushmuomala va professional tarzda javob berish.
Qoidalar:
1. Faqat mebel, yetkazib berish, narxlar va do'kon haqidagi savollarga javob ber.
2. Boshqa mavzulardagi savollarga "Kechirasiz, men faqat mebelga oid savollarga javob bera olaman" deb javob qaytar.
3. Hech qachon "Men sun'iy intellektman" dema, o'zingni virtual yordamchi deb tanishtir.
4. {categories_prompt}
   - Yetkazib berish Toshkent shahri ichida 24 soatda amalga oshiriladi."""]
        },
        {
            "role": "model",
            "parts": ["Tushunarli. Men 'ASMEBEL' do'konining virtual yordamchisiman. Mijozlarga mebel tanlashda yordam berishga tayyorman."]
        }
    ])
except Exception as e:
    logger.error(f"Gemini initsializatsiyasida xatolik: {e}")
    chat = None


async def get_gemini_response(user_message: str) -> str:
    if not chat:
        logger.warning("Gemini chat sessiyasi mavjud emas")
        return "Kechirasiz, AI xizmati hozirda mavjud emas. Iltimos, administrator bilan bog'lanishni o'ylab ko'ring."

    if not user_message or not user_message.strip():
        logger.warning("Bo'sh xabar yuborildi")
        return "Iltimos, savol yoki xabar kiriting."

    try:
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(None, lambda: chat.send_message(user_message))

        if not response or not response.text:
            logger.warning("Gemini bo'sh javob qaytardi")
            return "Kechirasiz, javob olib bo'lmadi. Qayta urinib ko'ring."

        return response.text
    except asyncio.CancelledError:
        logger.error("Gemini so'rovi bekor qilindi")
        return "So'rov bekor qilindi. Qayta urinib ko'ring."
    except TimeoutError:
        logger.error("Gemini so'rovi vaqt tugadi")
        return "So'rov vaqti tugadi. Qayta urinib ko'ring."
    except Exception as e:
        logger.error(f"Gemini bilan bog'lanishda xatolik: {type(e).__name__}: {e}")
        return "Kechirasiz, hozirda tizimda vaqtinchalik nosozlik mavjud. Iltimos, birozdan so'ng qayta urinib ko'ring."
