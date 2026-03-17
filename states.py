from aiogram.fsm.state import State, StatesGroup

class FormStates(StatesGroup):
    """Anketa to'ldirish holatlari"""
    job_type = State()
    name = State()
    age = State()
    education = State()
    previous_work = State()
    current_status = State()
    address = State()
    photo = State()
    phone = State()

class AdminStates(StatesGroup):
    """Admin holatlari"""
    vacancy_text = State()
    search_query = State()

class ContactStates(StatesGroup):
    """Adminga murojaat holatlari"""
    contact_type = State()  # Taklif yoki savol tanlash
    message = State()

class MedicineOrderStates(StatesGroup):
    """Dori buyurtma holatlari"""
    order_type = State()  # Retsepli, retsepsiz, tayyorlanadigan
    message = State()  # Xabar yoki rasm

class ReplyStates(StatesGroup):
    """Admin javob berish holatlari"""
    user_id = State()
    message = State()

class UserReplyStates(StatesGroup):
    """Foydalanuvchi admin javobiga javob berish holatlari"""
    admin_message_id = State()
    message = State()
    