# Burj Apteka Ishga Qabul Qilish Boti

Telegram bot ishga qabul qilish jarayonini avtomatlashtirish uchun.

## O'rnatish

1. Virtual muhit yarating:
```bash
python -m venv .venv
```

2. Virtual muhitni faollashtiring:
```bash
# Windows
.venv\Scripts\activate

# Linux/Mac
source .venv/bin/activate
```

3. Kerakli kutubxonalarni o'rnating:
```bash
pip install -r requirements.txt
```

4. `.env` faylini sozlang (allaqachon tayyor)

## Ishga tushirish

```bash
python main.py
```

## Funksiyalar

### Foydalanuvchilar uchun:
- 📝 Anketa to'ldirish (7 bosqichda)
- ℹ️ Bot haqida ma'lumot
- ✅ Ma'lumotlarni tasdiqlash va yuborish
- 🔄 Anketani qayta to'ldirish

### Admin uchun:
- 📢 Vakansiya e'lon qilish
- 📊 Statistika ko'rish
- 📨 Anketalarni qabul qilish

## Struktura

- `main.py` - Asosiy fayl
- `handlers.py` - Barcha handlerlar
- `keyboards.py` - Klaviaturalar
- `states.py` - FSM holatlari
- `database.py` - Ma'lumotlar saqlash
- `config.py` - Konfiguratsiya
- `.env` - Muhit o'zgaruvchilari

## Texnologiyalar

- aiogram 3.3.0
- python-dotenv 1.0.0
