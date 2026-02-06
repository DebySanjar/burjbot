from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID
from states import FormStates, VacancyStates, AdminStates
from keyboards import (
    main_menu, cancel_keyboard, confirm_keyboard, admin_keyboard,
    phone_keyboard, search_filter_keyboard, job_types_keyboard,
    vacancy_confirm_keyboard
)
import database

router = Router()

# Ish turlari nomlari
JOB_NAMES = {
    "operator": "💊 Operator",
    "farrosh": "🧹 Farrosh",
    "delivery": "🚚 Yetkazib beruvchi",
    "warehouse": "📦 Omborchi",
    "other": "💼 Boshqa"
}

# ==================== ASOSIY KOMANDALAR ====================

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Start komandasi"""
    user_id = message.from_user.id
    database.add_user_id(user_id)
    
    if user_id == ADMIN_ID:
        await message.answer(
            "👋 Assalomu alaykum, Admin!\n\n"
            "Siz admin panelidasiz.",
            reply_markup=admin_keyboard()
        )
    else:
        # Mavjud vakansiyalarni ko'rsatish
        vacancies = database.get_vacancies()
        if vacancies:
            text = "👋 Assalomu alaykum!\n\n📢 <b>Mavjud vakansiyalar:</b>\n\n"
            for job_type, vacancy_text in vacancies.items():
                text += f"━━━━━━━━━━━━━━━\n{vacancy_text}\n\n"
            text += "📝 Anketa to'ldirish uchun tugmani bosing."
        else:
            text = "👋 Assalomu alaykum!\n\nHozircha vakansiyalar yo'q."
        
        await message.answer(text, parse_mode="HTML", reply_markup=main_menu())

@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message):
    """Bot haqida ma'lumot"""
    await message.answer(
        "🤖 <b>Bot haqida</b>\n\n"
        "Bu bot Burj Apteka uchun ishga qabul qilish jarayonini "
        "avtomatlashtirish maqsadida yaratilgan.\n\n"
        "📝 Bot orqali siz:\n"
        "• Anketa to'ldirishingiz\n"
        "• O'z ma'lumotlaringizni yuborishingiz\n"
        "• Tezkor javob olishingiz mumkin\n\n"
        "📞 Savollar bo'lsa, admin bilan bog'laning.",
        parse_mode="HTML",
        reply_markup=main_menu()
    )

# ==================== ANKETA TO'LDIRISH ====================

@router.message(F.text == "📝 Anketa to'ldirish")
async def start_form(message: Message, state: FSMContext):
    """Anketa to'ldirishni boshlash - avval ish turini tanlash"""
    vacancies = database.get_vacancies()
    
    if not vacancies:
        await message.answer(
            "❌ Hozircha vakansiyalar yo'q.\n\n"
            "Keyinroq qayta urinib ko'ring.",
            reply_markup=main_menu()
        )
        return
    
    await state.set_state(FormStates.job_type)
    await message.answer(
        "📝 <b>Anketa to'ldirish</b>\n\n"
        "Qaysi lavozim uchun ariza topshirmoqchisiz?",
        parse_mode="HTML",
        reply_markup=job_types_keyboard()
    )

@router.callback_query(F.data.startswith("job_"))
async def process_job_type(callback: CallbackQuery, state: FSMContext):
    """Ish turini tanlash"""
    job_type = callback.data.replace("job_", "")
    job_name = JOB_NAMES.get(job_type, "Boshqa")
    
    await state.update_data(job_type=job_type, job_name=job_name)
    await state.set_state(FormStates.name)
    
    await callback.message.answer(
        f"✅ Tanlandi: {job_name}\n\n"
        "1️⃣ Ismingizni kiriting:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.message(FormStates.name)
async def process_name(message: Message, state: FSMContext):
    """Ism qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(name=message.text)
    await state.set_state(FormStates.age)
    await message.answer(
        "2️⃣ Yoshingizni kiriting:",
        reply_markup=cancel_keyboard()
    )

@router.message(FormStates.age)
async def process_age(message: Message, state: FSMContext):
    """Yosh qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(age=message.text)
    await state.set_state(FormStates.photo)
    await message.answer(
        "3️⃣ Rasmingizni yuboring:",
        reply_markup=cancel_keyboard()
    )

@router.message(FormStates.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    """Rasm qabul qilish"""
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await state.set_state(FormStates.family_status)
    await message.answer(
        "4️⃣ Oilaviy sharoitingizni kiriting:\n"
        "(masalan: oilaviy yoki turmush qurmagan)",
        reply_markup=cancel_keyboard()
    )

@router.message(FormStates.photo)
async def process_photo_invalid(message: Message, state: FSMContext):
    """Noto'g'ri format"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    await message.answer("❌ Iltimos, rasm yuboring!")

@router.message(FormStates.family_status)
async def process_family_status(message: Message, state: FSMContext):
    """Oilaviy holat qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(family_status=message.text)
    await state.set_state(FormStates.work_experience)
    await message.answer(
        "5️⃣ Avval qayerda ishlagansiz?\n"
        "(Ish tajribangiz yoki manzil)",
        reply_markup=cancel_keyboard()
    )

@router.message(FormStates.work_experience)
async def process_work_experience(message: Message, state: FSMContext):
    """Ish tajribasi qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(work_experience=message.text)
    await state.set_state(FormStates.salary)
    await message.answer(
        "6️⃣ Boshlanishiga qancha oylik maosh hohlayapsiz?",
        reply_markup=cancel_keyboard()
    )

@router.message(FormStates.salary)
async def process_salary(message: Message, state: FSMContext):
    """Maosh qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(salary=message.text)
    await state.set_state(FormStates.phone)
    await message.answer(
        "7️⃣ Telefon raqamingizni yuboring:\n\n"
        "📱 Kontakt ulashish tugmasini bosing yoki raqamni yozing.",
        reply_markup=phone_keyboard()
    )

@router.message(FormStates.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Kontakt orqali telefon qabul qilish"""
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    
    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    
    # Ma'lumotlarni formatlash
    summary = (
        "📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"💼 <b>Lavozim:</b> {data['job_name']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"💑 <b>Oilaviy holat:</b> {data['family_status']}\n"
        f"💼 <b>Ish tajribasi:</b> {data['work_experience']}\n"
        f"� o<b>Kutilayotgan maosh:</b> {data['salary']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )
    
    # Rasmni yuborish
    await message.answer_photo(
        photo=data['photo'],
        caption=summary,
        parse_mode="HTML",
        reply_markup=confirm_keyboard()
    )

@router.message(FormStates.phone)
async def process_phone_text(message: Message, state: FSMContext):
    """Matn orqali telefon qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=main_menu())
        return
    
    await state.update_data(phone=message.text)
    
    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    
    # Ma'lumotlarni formatlash
    summary = (
        "📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"💼 <b>Lavozim:</b> {data['job_name']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"💑 <b>Oilaviy holat:</b> {data['family_status']}\n"
        f"💼 <b>Ish tajribasi:</b> {data['work_experience']}\n"
        f"💰 <b>Kutilayotgan maosh:</b> {data['salary']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )
    
    # Rasmni yuborish
    await message.answer_photo(
        photo=data['photo'],
        caption=summary,
        parse_mode="HTML",
        reply_markup=confirm_keyboard()
    )

# ==================== TASDIQLASH ====================

@router.callback_query(F.data == "confirm_send")
async def confirm_send(callback: CallbackQuery, state: FSMContext, bot):
    """Ma'lumotlarni adminga yuborish"""
    data = await state.get_data()
    user = callback.from_user
    
    # Foydalanuvchi ma'lumotlarini saqlash
    database.save_user(user.id, data)
    
    # Admin uchun xabar
    username = user.username if user.username else "Yo'q"
    admin_message = (
        "📨 <b>Yangi anketa!</b>\n\n"
        f"💼 <b>Lavozim:</b> {data['job_name']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"💑 <b>Oilaviy holat:</b> {data['family_status']}\n"
        f"💼 <b>Ish tajribasi:</b> {data['work_experience']}\n"
        f"💰 <b>Kutilayotgan maosh:</b> {data['salary']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        f"🆔 <b>Telegram ID:</b> {user.id}\n"
        f"👨‍💼 <b>Username:</b> @{username}"
    )
    
    # Adminga yuborish
    await bot.send_photo(
        chat_id=ADMIN_ID,
        photo=data['photo'],
        caption=admin_message,
        parse_mode="HTML"
    )
    
    # Foydalanuvchiga tasdiqlash
    await callback.message.answer(
        "✅ Ma'lumotlaringiz muvaffaqiyatli yuborildi!\n\n"
        "Tez orada siz bilan bog'lanamiz. 😊",
        reply_markup=main_menu()
    )
    
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "restart_form")
async def restart_form(callback: CallbackQuery, state: FSMContext):
    """Anketani qayta to'ldirish"""
    await state.clear()
    await state.set_state(FormStates.job_type)
    await callback.message.answer(
        "🔄 Anketani qayta to'ldiring.\n\n"
        "Qaysi lavozim uchun ariza topshirmoqchisiz?",
        reply_markup=job_types_keyboard()
    )
    await callback.answer()

# ==================== ADMIN - VAKANSIYA E'LON QILISH ====================

@router.message(F.text == "📢 Vakansiya e'lon qilish")
async def admin_vacancy_start(message: Message, state: FSMContext):
    """Vakansiya e'lon qilishni boshlash"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    
    await state.set_state(VacancyStates.job_type)
    await message.answer(
        "📢 <b>Vakansiya e'lon qilish</b>\n\n"
        "1️⃣ Ish turini kiriting:\n"
        "(masalan: Operator, Farrosh, Yetkazib beruvchi)",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.job_type)
async def process_vacancy_job_type(message: Message, state: FSMContext):
    """Ish turini qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(job_type=message.text)
    await state.set_state(VacancyStates.location)
    await message.answer(
        "2️⃣ Manzilni kiriting:",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.location)
async def process_vacancy_location(message: Message, state: FSMContext):
    """Manzilni qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(location=message.text)
    await state.set_state(VacancyStates.time)
    await message.answer(
        "3️⃣ Ish vaqtini kiriting:\n"
        "(masalan: 9:00-18:00, smenali)",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.time)
async def process_vacancy_time(message: Message, state: FSMContext):
    """Vaqtni qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(time=message.text)
    await state.set_state(VacancyStates.salary)
    await message.answer(
        "4️⃣ Maoshni kiriting:\n"
        "(masalan: 3,000,000 - 5,000,000 so'm)",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.salary)
async def process_vacancy_salary(message: Message, state: FSMContext):
    """Maoshni qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(salary=message.text)
    await state.set_state(VacancyStates.age_limit)
    await message.answer(
        "5️⃣ Xodim yosh chegarasini kiriting:\n"
        "(masalan: 18-35 yosh)",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.age_limit)
async def process_vacancy_age_limit(message: Message, state: FSMContext):
    """Yosh chegarasini qabul qilish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(age_limit=message.text)
    await state.set_state(VacancyStates.additional)
    await message.answer(
        "6️⃣ Qo'shimcha ma'lumot kiriting:\n"
        "(masalan: Talablar, imtiyozlar)",
        reply_markup=cancel_keyboard()
    )

@router.message(VacancyStates.additional)
async def process_vacancy_additional(message: Message, state: FSMContext):
    """Qo'shimcha ma'lumotni qabul qilish va ko'rsatish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    await state.update_data(additional=message.text)
    
    # Barcha ma'lumotlarni olish
    data = await state.get_data()
    
    # Vakansiya matnini formatlash
    vacancy_text = (
        f"📢 <b>{data['job_type']}</b>\n\n"
        f"📍 <b>Manzil:</b> {data['location']}\n"
        f"🕐 <b>Ish vaqti:</b> {data['time']}\n"
        f"💰 <b>Maosh:</b> {data['salary']}\n"
        f"👥 <b>Yosh:</b> {data['age_limit']}\n"
        f"📝 <b>Qo'shimcha:</b> {data['additional']}\n\n"
        f"📞 Ariza topshirish uchun /start bosing!"
    )
    
    await message.answer(
        "📋 <b>Vakansiya ko'rinishi:</b>\n\n" + vacancy_text + "\n\n"
        "Ma'lumotlar to'g'rimi?",
        parse_mode="HTML",
        reply_markup=vacancy_confirm_keyboard()
    )

@router.callback_query(F.data == "confirm_vacancy")
async def confirm_vacancy(callback: CallbackQuery, state: FSMContext, bot):
    """Vakansiyani tasdiqlash va e'lon qilish"""
    data = await state.get_data()
    
    # Vakansiya matnini formatlash
    vacancy_text = (
        f"📢 <b>{data['job_type']}</b>\n\n"
        f"📍 <b>Manzil:</b> {data['location']}\n"
        f"🕐 <b>Ish vaqti:</b> {data['time']}\n"
        f"💰 <b>Maosh:</b> {data['salary']}\n"
        f"👥 <b>Yosh:</b> {data['age_limit']}\n"
        f"📝 <b>Qo'shimcha:</b> {data['additional']}"
    )
    
    # Vakansiyani saqlash
    job_type_key = data['job_type'].lower().replace(" ", "_")
    database.set_vacancy(job_type_key, vacancy_text)
    
    # Barcha foydalanuvchilarga yuborish
    user_ids = database.get_all_user_ids()
    success_count = 0
    
    for user_id in user_ids:
        if user_id == ADMIN_ID:
            continue
        try:
            await bot.send_message(
                chat_id=user_id,
                text=f"📢 <b>Yangi vakansiya e'loni!</b>\n\n{vacancy_text}",
                parse_mode="HTML"
            )
            success_count += 1
        except Exception:
            pass
    
    await callback.message.answer(
        f"✅ Vakansiya e'lon qilindi!\n\n"
        f"📤 {success_count} ta foydalanuvchiga yuborildi.",
        reply_markup=admin_keyboard()
    )
    
    await callback.answer()
    await state.clear()

@router.callback_query(F.data == "restart_vacancy")
async def restart_vacancy(callback: CallbackQuery, state: FSMContext):
    """Vakansiyani qayta yozish"""
    await state.clear()
    await state.set_state(VacancyStates.job_type)
    await callback.message.answer(
        "🔄 Vakansiyani qayta yozing.\n\n"
        "1️⃣ Ish turini kiriting:",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

# ==================== ADMIN - STATISTIKA ====================

@router.message(F.text == "📊 Statistika")
async def admin_stats(message: Message):
    """Statistika"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    
    users_count = database.get_users_count()
    all_users = database.get_all_users()
    applications_count = len(all_users)
    vacancies = database.get_vacancies()
    vacancies_count = len(vacancies)
    
    await message.answer(
        f"📊 <b>Statistika</b>\n\n"
        f"👥 Jami foydalanuvchilar: {users_count}\n"
        f"📝 Anketa yuborgan: {applications_count}\n"
        f"📢 Vakansiyalar: {vacancies_count}",
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )

# ==================== ADMIN - QIDIRUV ====================

@router.message(F.text == "🔍 Foydalanuvchilarni qidirish")
async def search_users_menu(message: Message):
    """Qidiruv menyusi"""
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    
    await message.answer(
        "🔍 <b>Qidiruv</b>\n\n"
        "Qidiruv turini tanlang:",
        parse_mode="HTML",
        reply_markup=search_filter_keyboard()
    )

@router.callback_query(F.data.startswith("search_by_"))
async def search_filter_selected(callback: CallbackQuery, state: FSMContext):
    """Qidiruv turi tanlandi"""
    search_type = callback.data.split("_")[-1]
    
    search_names = {
        "name": "👤 Ism",
        "phone": "📞 Telefon",
        "location": "📍 Ish tajribasi"
    }
    
    await state.set_state(AdminStates.search_query)
    await state.update_data(search_type=search_type)
    
    await callback.message.answer(
        f"🔍 <b>{search_names[search_type]} bo'yicha qidirish</b>\n\n"
        f"Qidiruv so'zini kiriting:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "cancel_search")
async def cancel_search(callback: CallbackQuery):
    """Qidiruvni bekor qilish"""
    await callback.message.answer(
        "❌ Qidiruv bekor qilindi.",
        reply_markup=admin_keyboard()
    )
    await callback.answer()

@router.message(AdminStates.search_query)
async def process_search_query(message: Message, state: FSMContext):
    """Qidiruv so'rovini qayta ishlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Qidiruv bekor qilindi.", reply_markup=admin_keyboard())
        return
    
    query = message.text
    results = database.search_users(query)
    
    if not results:
        await message.answer(
            "❌ Hech narsa topilmadi.\n\n"
            "Boshqa so'z bilan qidiring yoki /start bosing.",
            reply_markup=cancel_keyboard()
        )
        return
    
    # Natijalarni ko'rsatish
    response = f"🔍 <b>Qidiruv natijalari:</b>\n\n"
    response += f"Topildi: {len(results)} ta\n\n"
    
    for i, (user_id, data) in enumerate(results[:10], 1):
        response += (
            f"{i}. 💼 <b>{data.get('job_name', 'N/A')}</b>\n"
            f"   👤 {data['name']}\n"
            f"   📞 {data['phone']}\n"
            f"   💼 {data['work_experience']}\n"
            f"   🆔 ID: <code>{user_id}</code>\n\n"
        )
    
    if len(results) > 10:
        response += f"... va yana {len(results) - 10} ta natija"
    
    await message.answer(
        response,
        parse_mode="HTML",
        reply_markup=admin_keyboard()
    )
    
    await state.clear()
