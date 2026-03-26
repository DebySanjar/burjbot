from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def main_menu():
    """Asosiy menyu"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💊 Dori buyurtma berish")],
            [KeyboardButton(text="📞 Murojaat qilish")],
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
    """Tasdiqlash tugmalari - Modern dizayn"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="✅ Yuborish", callback_data="confirm_send"),
                InlineKeyboardButton(text="🔄 Qaytadan", callback_data="restart_form")
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
    """Admin paneli - Modern dizayn"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📢 Vakansiya e'lon qilish")],
            [
                KeyboardButton(text="🔍 Qidirish"), 
                KeyboardButton(text="📊 Statistika")
            ]
        ],
        resize_keyboard=True
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

def reply_to_user_keyboard(user_id):
    """Foydalanuvchiga javob berish tugmasi"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Javob berish", callback_data=f"reply_{user_id}")]
        ]
    )
    return keyboard

def about_bot_keyboard():
    """Bot haqida inline tugmalari - faqat info"""
    # Bu keyboard endi bo'sh, chunki "Adminga murojaat" alohida tugma bo'ldi
    return None

def search_filter_keyboard():
    """Qidiruv filtri tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Ism bo'yicha", callback_data="search_by_name")],
            [InlineKeyboardButton(text="📞 Telefon bo'yicha", callback_data="search_by_phone")],
            [InlineKeyboardButton(text="📍 Manzil bo'yicha", callback_data="search_by_address")],
            [InlineKeyboardButton(text="💼 Ish tajribasi bo'yicha", callback_data="search_by_work")],
            [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="cancel_search")]
        ]
    )
    return keyboard

def job_types_keyboard():
    """Ish turlari ro'yxati"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=" Operator", callback_data="job_operator")],
            [InlineKeyboardButton(text=" Sotuvchi", callback_data="job_sotuvchi")],
            [InlineKeyboardButton(text=" Dori tayyorlash", callback_data="job_dori")],
            [InlineKeyboardButton(text="🧹 Farrosh", callback_data="job_farrosh")]
        ]
    )
    return keyboard

def contact_options_keyboard():
    """Murojaat qilish variantlari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💡 Taklif yuborish", callback_data="contact_suggestion")],
            [InlineKeyboardButton(text="❓ Savol yuborish", callback_data="contact_question")],
            [InlineKeyboardButton(text="⚠️ Shikoyat qilish", callback_data="contact_complaint")]
        ]
    )
    return keyboard

def complaint_options_keyboard():
    """Shikoyat turlari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💊 Dori yuzasidan shikoyat", callback_data="complaint_medicine")],
            [InlineKeyboardButton(text="👤 Xodim ustidan shikoyat", callback_data="complaint_staff")]
        ]
    )
    return keyboard

def medicine_order_keyboard():
    """Dori buyurtma variantlari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚗️ Tayyorlanadigan dori vositalari", callback_data="medicine_custom")],
            [InlineKeyboardButton(text="🏥 Tibbiy buyum va texnikalar", callback_data="medicine_medical_equipment")],
            [InlineKeyboardButton(text="📋 Retsepli dori vositalari", callback_data="medicine_prescription")],
            [InlineKeyboardButton(text="💊 Retsepsiz dori vositalari", callback_data="medicine_no_prescription")]
        ]
    )
    return keyboard
def user_reply_keyboard():
    """Foydalanuvchi admin javobiga javob berish tugmasi"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 Javob berish", callback_data="user_reply")]
        ]
    )
    return keyboard

def channel_subscription_keyboard(channel_url):
    """Kanalga a'zo bo'lish tugmalari"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📢 Kanalga qo'shilish", url=channel_url)],
            [InlineKeyboardButton(text="✅ Tekshirish", callback_data="check_subscription")]
        ]
    )
    return keyboard