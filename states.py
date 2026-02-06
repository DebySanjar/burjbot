from aiogram.fsm.state import State, StatesGroup

class FormStates(StatesGroup):
    """Anketa to'ldirish holatlari"""
    job_type = State()  # Ish turi tanlash
    name = State()
    age = State()
    photo = State()
    family_status = State()
    work_experience = State()
    salary = State()
    phone = State()

class VacancyStates(StatesGroup):
    """Vakansiya e'lon qilish holatlari"""
    job_type = State()  # Ish turi
    location = State()  # Manzil
    time = State()  # Vaqt
    salary = State()  # Maosh
    age_limit = State()  # Yosh chegarasi
    additional = State()  # Qo'shimcha

class AdminStates(StatesGroup):
    """Admin holatlari"""
    search_query = State()
