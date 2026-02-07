from aiogram.fsm.state import State, StatesGroup

class FormStates(StatesGroup):
    """Anketa to'ldirish holatlari"""
    job_type = State()
    name = State()
    age = State()
    address = State()
    photo = State()
    family_status = State()
    work_experience = State()
    salary = State()
    phone = State()

class AdminStates(StatesGroup):
    """Admin holatlari"""
    vacancy_text = State()
    search_query = State()

class ContactStates(StatesGroup):
    """Adminga murojaat holatlari"""
    message = State()

class ReplyStates(StatesGroup):
    """Admin javob berish holatlari"""
    user_id = State()
    message = State()
