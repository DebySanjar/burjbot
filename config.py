import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '8638136717:AAE5GlDzWsnCnQ_XYTnMXiXRhdXG_5ibKwI')
ADMIN_ID = int(os.getenv('ADMIN_ID', '1961347582'))  # Asosiy admin
SUPER_ADMIN_ID = 62791591  # Super admin
MEDICINE_ADMIN_ID = 6502918946  # Dori buyurtma admin

# Barcha adminlar ro'yxati
ALL_ADMINS = [ADMIN_ID, SUPER_ADMIN_ID, MEDICINE_ADMIN_ID]

# Majburiy kanal
CHANNEL_ID = "@Burj_spravichniy"  # Kanal username
CHANNEL_URL = "https://t.me/Burj_spravichniy"  # Kanal linki

# Xatoliklarni tekshirish

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID topilmadi! .env faylini tekshiring.")
