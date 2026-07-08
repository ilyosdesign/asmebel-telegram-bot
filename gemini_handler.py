# gemini_handler.py

from google.generativeai.client import configure
from google.generativeai.generative_models import GenerativeModel
from config import GEMINI_API_KEY
from products import get_categories_for_prompt

# Gemini API ni sozlash
configure(api_key=GEMINI_API_KEY)

model = GenerativeModel(model_name="gemini-1.5-pro-latest")

# Gemini uchun kategoriya ro'yxatini olish
categories_prompt = get_categories_for_prompt()

# Chat sessiyasini boshlash va botga "shaxsiyatini" berish
# SIZNING SKRIPTLARINGIZ SHU YERDA BOSHLANADI
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


async def get_gemini_response(user_message: str) -> str:
    """
    Foydalanuvchi xabarini Gemini'ga yuboradi va javobini oladi.
    """
    try:
        response = chat.send_message(user_message)
        return response.text
    except Exception as e:
        print(f"Gemini bilan bog'lanishda xatolik: {e}")
        return "Kechirasiz, hozirda tizimda vaqtinchalik nosozlik mavjud. Iltimos, birozdan so'ng qayta urinib ko'ring."
