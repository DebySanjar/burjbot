"""Ma'lumotlarni saqlash uchun oddiy modul"""

# Vakansiyalar ro'yxati
vacancies = {}  # {job_type: vacancy_text}

# Foydalanuvchilar ro'yxati
users = {}  # {user_id: {'name': '', 'age': '', 'phone': '', ...}}

# Barcha foydalanuvchi ID lari
all_user_ids = set()

def get_vacancies():
    """Barcha vakansiyalarni olish"""
    return vacancies

def get_vacancy(job_type):
    """Ma'lum ish turi uchun vakansiyani olish"""
    return vacancies.get(job_type)

def set_vacancy(job_type, text):
    """Vakansiyani saqlash"""
    vacancies[job_type] = text

def add_user_id(user_id):
    """Foydalanuvchi ID sini saqlash"""
    all_user_ids.add(user_id)

def get_all_user_ids():
    """Barcha foydalanuvchi ID larini olish"""
    return list(all_user_ids)

def save_user(user_id, data):
    """Foydalanuvchi ma'lumotlarini saqlash"""
    users[user_id] = data

def get_user(user_id):
    """Foydalanuvchi ma'lumotlarini olish"""
    return users.get(user_id)

def search_users(query):
    """Foydalanuvchilarni qidirish"""
    query = query.lower()
    results = []
    
    for user_id, data in users.items():
        # Ism bo'yicha qidirish
        if query in data.get('name', '').lower():
            results.append((user_id, data))
        # Telefon bo'yicha qidirish
        elif query in data.get('phone', '').lower():
            results.append((user_id, data))
        # Ish tajribasi (manzil) bo'yicha qidirish
        elif query in data.get('work_experience', '').lower():
            results.append((user_id, data))
    
    return results

def get_users_count():
    """Foydalanuvchilar sonini olish"""
    return len(all_user_ids)

def get_all_users():
    """Barcha foydalanuvchilarni olish"""
    return users
