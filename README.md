# Burj Apteka Ishga Qabul Qilish Boti

Telegram bot ishga qabul qilish jarayonini avtomatlashtirish uchun.

## Railway Deploy

### 1. GitHub'ga yuklash

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-repo-url>
git push -u origin main
```

### 2. Railway'da sozlash

1. Railway.app'ga kiring
2. "New Project" > "Deploy from GitHub repo"
3. Repository'ni tanlang
4. Environment Variables qo'shing:
   - `BOT_TOKEN`: 7979034038:AAGs3G1CtNZjju5acfdCMMHbbVwE7yDH7Qc
   - `ADMIN_ID`: 7176985245

### 3. Deploy

Railway avtomatik deploy qiladi. Loglarni tekshiring.

## Lokal ishga tushirish

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

4. `.env` faylini sozlang

5. Botni ishga tushiring:
```bash
python main.py
```

## Funksiyalar

### Foydalanuvchilar uchun:
- 📝 Anketa to'ldirish (7 bosqichda)
- 📱 Kontakt ulashish
- ℹ️ Bot haqida ma'lumot
- ✅ Ma'lumotlarni tasdiqlash va yuborish

### Admin uchun:
- 📢 Vakansiya e'lon qilish (barcha foydalanuvchilarga)
- 🔍 Foydalanuvchilarni qidirish (ism, telefon, ish tajribasi)
- 📊 Statistika ko'rish
- 👤 Foydalanuvchi rejimiga o'tish
- 📨 Anketalarni qabul qilish

## Texnologiyalar

- aiogram 3.15.0
- python-dotenv 1.0.1
- Python 3.11
