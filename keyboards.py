from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """Asosiy menyu"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Anketa to'ldirish")],
            [KeyboardButton(text="ℹ️ Bot haqida")]
        ],
        resize_keyboard=True
    )
    return keyboard

def cancel_keyboard():
    """Bekor qilish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="❌ Bekor qilish")]],
        resize_keyboard=True
    )
    return keyboard

def phone_keyboard():
    """Telefon raqam ulashish tugmasi"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Kontakt ulashish", request_contact=True)],
            [KeyboardButton(text="❌ Bekor qilish")]
        ],
        resize_keyboard=True
    )
    return keyboard

def confirm_keyboard():
    """Tasdiqlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yuborish", callback_data="confirm_send"),
                InlineKeyboardButton(text="🔄 Qayta to'ldirish", callback_data="restart_form")
            ]
        ]
    )
    return keyboard

def vacancy_confirm_keyboard():
    """Vakansiya tasdiqlash tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ E'lon qilish", callback_data="confirm_vacancy"),
                InlineKeyboardButton(text="🔄 Qayta yozish", callback_data="restart_vacancy")
            ]
        ]
    )
    return keyboard

def admin_keyboard():
    """Admin paneli"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📢 Vakansiya e'lon qilish")],
            [KeyboardButton(text="🔍 Foydalanuvchilarni qidirish")],
            [KeyboardButton(text="📊 Statistika")]
        ],
        resize_keyboard=True
    )
    return keyboard

def search_filter_keyboard():
    """Qidiruv filtri tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Ism bo'yicha", callback_data="search_by_name")],
            [InlineKeyboardButton(text="📞 Telefon bo'yicha", callback_data="search_by_phone")],
            [InlineKeyboardButton(text="📍 Ish tajribasi bo'yicha", callback_data="search_by_location")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_search")]
        ]
    )
    return keyboard

def job_types_keyboard():
    """Ish turlari ro'yxati"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💊 Operator", callback_data="job_operator")],
            [InlineKeyboardButton(text="🧹 Farrosh", callback_data="job_farrosh")],
            [InlineKeyboardButton(text="🚚 Yetkazib beruvchi", callback_data="job_delivery")],
            [InlineKeyboardButton(text="📦 Omborchi", callback_data="job_warehouse")],
            [InlineKeyboardButton(text="💼 Boshqa", callback_data="job_other")]
        ]
    )
    return keyboard
