import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN', '7979034038:AAGs3G1CtNZjju5acfdCMMHbbVwE7yDH7Qc')
ADMIN_ID = int(os.getenv('ADMIN_ID', '869927958'))

# Xatoliklarni tekshirish
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN topilmadi! .env faylini tekshiring.")

if not ADMIN_ID:
    raise ValueError("ADMIN_ID topilmadi! .env faylini tekshiring.")
