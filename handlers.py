from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from config import ADMIN_ID, CHANNEL_ID, CHANNEL_URL, SUPER_ADMIN_ID, MEDICINE_ADMIN_ID, ALL_ADMINS
from states import FormStates, AdminStates, ContactStates, ReplyStates, MedicineOrderStates, UserReplyStates
from keyboards import (
    main_menu, cancel_keyboard, confirm_keyboard, admin_keyboard,
    phone_keyboard, search_filter_keyboard, about_bot_keyboard,
    vacancy_confirm_keyboard, reply_to_user_keyboard, job_types_keyboard,
    contact_options_keyboard, channel_subscription_keyboard, medicine_order_keyboard,
    user_reply_keyboard, complaint_options_keyboard
)
import database
from job_names import JOB_NAMES

router = Router()
admin_mode = {}


def is_admin(user_id):
    """Foydalanuvchi admin ekanligini tekshirish"""
    return user_id in ALL_ADMINS


def is_super_admin(user_id):
    """Foydalanuvchi super admin ekanligini tekshirish"""
    return user_id == SUPER_ADMIN_ID


def is_medicine_admin(user_id):
    """Foydalanuvchi dori admin ekanligini tekshirish"""
    return user_id == MEDICINE_ADMIN_ID or user_id == SUPER_ADMIN_ID


async def check_user_subscription(bot, user_id):
    """Foydalanuvchi kanalga a'zo ekanligini tekshirish"""
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        # left va kicked - a'zo emas, qolganlar a'zo
        return member.status not in ['left', 'kicked']
    except Exception as e:
        print(f"A'zolikni tekshirishda xatolik: {e}")
        # Xatolik bo'lsa (bot kanalda admin emas yoki boshqa sabab)
        # Foydalanuvchiga ruxsat beramiz
        return True


async def subscription_required(message_or_callback, bot):
    """A'zolik talab qilinadi - umumiy funksiya"""
    user_id = message_or_callback.from_user.id

    # Admin uchun a'zolik tekshiruvi yo'q
    if user_id == ADMIN_ID:
        return True

    is_subscribed = await check_user_subscription(bot, user_id)

    if not is_subscribed:
        text = (
            "🔒 <b>Kanalga qo'shiling!</b>\n\n"
            "📢 Botdan foydalanish uchun rasmiy kanalimizga a'zo bo'ling.\n\n"
            "✨ A'zo bo'lgandan keyin barcha imkoniyatlardan foydalaning!"
        )

        if hasattr(message_or_callback, 'answer'):  # Message
            await message_or_callback.answer(text, parse_mode="HTML",
                                             reply_markup=channel_subscription_keyboard(CHANNEL_URL))
        else:  # CallbackQuery
            await message_or_callback.message.answer(text, parse_mode="HTML",
                                                     reply_markup=channel_subscription_keyboard(CHANNEL_URL))
            await message_or_callback.answer()

        return False

    return True


@router.message(Command("cancel"))
async def cmd_cancel(message: Message, state: FSMContext):
    """Har qanday holatdan bekor qilish va bosh menyuga qaytish"""
    await state.clear()
    user_id = message.from_user.id
    is_admin = user_id == ADMIN_ID
    await message.answer(
        "❌ Bekor qilindi. Bosh menyuga qaytdingiz.",
        reply_markup=admin_keyboard() if is_admin else main_menu()
    )


@router.message(Command("help"))
async def cmd_help(message: Message, bot, state: FSMContext):
    """Bot haqida ma'lumot"""
    await state.clear()
    await message.answer(
        "🤖 <b>Burj Apteka - Rasmiy Xizmat Boti</b>\n\n"
        "🏥 <b>Biz haqimizda:</b>\n"
        "Burj Apteka - O'zbekistondagi yetakchi dorixonalar tarmog'i. Sifatli dori vositalari va professional xizmat ko'rsatish bilan mijozlarimizga xizmat qilamiz.\n\n"
        "📋 <b>Bot imkoniyatlari:</b>\n\n"
        "💊 <b>Dori buyurtma berish</b>\n"
        "   • Tibbiy buyum va texnikalar\n"
        "   • Tayyorlanadigan dori vositalari\n"
        "   • Retsepli dori vositalari\n"
        "   • Retsepsiz dori vositalari\n"
        "   Barcha buyurtmalar tezkor ko'rib chiqiladi va javob beriladi.\n\n"
        "📞 <b>Murojaat qilish</b>\n"
        "   • Taklif - Xizmatni yaxshilash bo'yicha fikrlaringiz\n"
        "   • Savol - Dorilar va xizmatlar haqida savollar\n"
        "   • Shikoyat - Dori yoki xodimlar ustidan shikoyatlar\n"
        "   Barcha murojaatlar diqqat bilan ko'rib chiqiladi.\n\n"
        "📝 <b>Anketa to'ldirish</b>\n"
        "   Bizning jamoamizga qo'shilishni istaysizmi? Anketa to'ldiring va biz siz bilan bog'lanamiz!\n\n"
        "📞 <b>Aloqa ma'lumotlari:</b>\n"
        "   Telefon: +998954040909\n"
        "   Telegram: @Burj_spravichniy\n\n"
        "⏰ <b>Ish tartibi:</b> 24/7 - Har doim xizmatdamiz!\n\n"
        "💬 Savollaringiz bo'lsa, bemalol murojaat qiling!",
        parse_mode="HTML"
    )


@router.message(Command("start"))
async def cmd_start(message: Message, bot):
    user_id = message.from_user.id
    database.add_user_id(user_id)

    # Adminlar uchun
    if is_admin(user_id):
        admin_type = "Super Admin" if is_super_admin(user_id) else (
            "Dori Admin" if is_medicine_admin(user_id) else "Admin")
        await message.answer(
            f"🔐 <b>{admin_type} Panel</b>\n\n"
            "👋 Assalomu alaykum!\n"
            "Boshqaruv paneliga xush kelibsiz.",
            parse_mode="HTML",
            reply_markup=admin_keyboard()
        )
        return

    # Oddiy foydalanuvchi uchun a'zolikni tekshirish
    is_subscribed = await check_user_subscription(bot, user_id)

    if not is_subscribed:
        await message.answer(
            "🔒 <b>Kanalga qo'shiling!</b>\n\n"
            "📢 Botdan foydalanish uchun rasmiy kanalimizga a'zo bo'ling.\n\n"
            "✨ A'zo bo'lgandan keyin barcha imkoniyatlardan foydalaning!",
            parse_mode="HTML",
            reply_markup=channel_subscription_keyboard(CHANNEL_URL)
        )
        return

    # A'zo bo'lsa, oddiy menyu
    vacancy_text = database.get_vacancy()
    welcome_text = (
        "🎉 <b>Xush kelibsiz!</b>\n\n"
        f"{vacancy_text}\n\n"
        "🚀 Quyidagi tugmalardan foydalaning:"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=main_menu())


@router.message(F.text == "ℹ️ Bot haqida")
async def about_bot(message: Message, bot, state: FSMContext):
    # Avval state'ni tozalaymiz
    await state.clear()

    if not await subscription_required(message, bot):
        return

    await message.answer(
        "🤖 <b>Burj Apteka - Rasmiy Xizmat Boti</b>\n\n"
        "🏥 <b>Biz haqimizda:</b>\n"
        "Burj Apteka - O'zbekistondagi yetakchi dorixonalar tarmog'i. Sifatli dori vositalari va professional xizmat ko'rsatish bilan mijozlarimizga xizmat qilamiz.\n\n"
        "📋 <b>Bot imkoniyatlari:</b>\n\n"
        "💊 <b>Dori buyurtma berish</b>\n"
        "   • Tibbiy buyum va texnikalar\n"
        "   • Tayyorlanadigan dori vositalari\n"
        "   • Retsepli dori vositalari\n"
        "   • Retsepsiz dori vositalari\n"
        "   Barcha buyurtmalar tezkor ko'rib chiqiladi va javob beriladi.\n\n"
        "📞 <b>Murojaat qilish</b>\n"
        "   • Taklif - Xizmatni yaxshilash bo'yicha fikrlaringiz\n"
        "   • Savol - Dorilar va xizmatlar haqida savollar\n"
        "   • Shikoyat - Dori yoki xodimlar ustidan shikoyatlar\n"
        "   Barcha murojaatlar diqqat bilan ko'rib chiqiladi.\n\n"
        "📝 <b>Anketa to'ldirish</b>\n"
        "   Bizning jamoamizga qo'shilishni istaysizmi? Anketa to'ldiring va biz siz bilan bog'lanamiz!\n\n"
        "📞 <b>Aloqa ma'lumotlari:</b>\n"
        "   Telefon: +998954040909\n"
        "   Telegram: @Burj_spravichniy\n\n"
        "⏰ <b>Ish tartibi:</b> 24/7 - Har doim xizmatdamiz!\n\n"
        "💬 Savollaringiz bo'lsa, bemalol murojaat qiling!",
        parse_mode="HTML"
    )


@router.message(F.text == "📝 Anketa to'ldirish")
async def start_form(message: Message, state: FSMContext, bot):
    # Avval state'ni tozalaymiz
    await state.clear()

    if not await subscription_required(message, bot):
        return

    await state.set_state(FormStates.job_type)
    await message.answer(
        "Ishlamoqchi bo'lgan ishingiz:",
        reply_markup=job_types_keyboard()
    )


@router.callback_query(F.data.startswith("job_"))
async def process_job_type_callback(callback: CallbackQuery, state: FSMContext):
    """Ish turini inline button orqali tanlash"""
    job_type = JOB_NAMES.get(callback.data, "Noma'lum")
    await state.update_data(job_type=job_type)
    await state.set_state(FormStates.name)
    await callback.message.answer("Ismingizni kiriting:", reply_markup=cancel_keyboard())
    await callback.answer()


@router.message(FormStates.job_type)
async def process_job_type_text(message: Message, state: FSMContext):
    """Agar text yuborilsa (bekor qilish)"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await message.answer("Iltimos, yuqoridagi tugmalardan birini tanlang:", reply_markup=job_types_keyboard())


@router.message(FormStates.name)
async def process_name(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(name=message.text)
    await state.set_state(FormStates.age)
    await message.answer("Yoshingizni kiriting:", reply_markup=cancel_keyboard())


@router.message(FormStates.age)
async def process_age(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(age=message.text)
    await state.set_state(FormStates.education)
    await message.answer("Ma'lumotingiz:\n(O'rta maxsus yoki oliy ma'lumot)", reply_markup=cancel_keyboard())


@router.message(FormStates.education)
async def process_education(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(education=message.text)
    await state.set_state(FormStates.previous_work)
    await message.answer("Avval ishlagan joyingiz:\n(Agar bo'lsa)", reply_markup=cancel_keyboard())


@router.message(FormStates.previous_work)
async def process_previous_work(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(previous_work=message.text)
    await state.set_state(FormStates.current_status)
    await message.answer("Hozirda o'qiysizmi yoki ishlaysizmi va qayerda?", reply_markup=cancel_keyboard())


@router.message(FormStates.current_status)
async def process_current_status(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(current_status=message.text)
    await state.set_state(FormStates.address)
    await message.answer("Manzilingizni kiriting:", reply_markup=cancel_keyboard())


@router.message(FormStates.address)
async def process_address(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await state.update_data(address=message.text)
    await state.set_state(FormStates.photo)
    await message.answer("Rasmingizni yuboring:", reply_markup=cancel_keyboard())


@router.message(FormStates.photo, F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(photo=photo_id)
    await state.set_state(FormStates.phone)
    await message.answer(
        "Telefon raqamingizni yuboring:\n\n📱 Kontakt ulashish tugmasini bosing yoki raqamni yozing.",
        reply_markup=phone_keyboard()
    )


@router.message(FormStates.photo)
async def process_photo_invalid(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return
    await message.answer("❌ Iltimos, rasm yuboring!")
    await state.set_state(FormStates.phone)
    await message.answer("Telefon raqamingizni yuboring:\n\n📱 Kontakt ulashish tugmasini bosing yoki raqamni yozing.",
                         reply_markup=phone_keyboard())


@router.message(FormStates.phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    phone = message.contact.phone_number
    await state.update_data(phone=phone)
    data = await state.get_data()

    summary = (
        "📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"💼 <b>Ish:</b> {data['job_type']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"🎓 <b>Ma'lumot:</b> {data['education']}\n"
        f"💼 <b>Avval ishlagan joy:</b> {data['previous_work']}\n"
        f"📚 <b>Hozirgi holat:</b> {data['current_status']}\n"
        f"📍 <b>Manzil:</b> {data['address']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )

    await message.answer_photo(photo=data['photo'], caption=summary, parse_mode="HTML", reply_markup=confirm_keyboard())


@router.message(FormStates.phone)
async def process_phone_text(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        user_id = message.from_user.id
        is_admin = user_id == ADMIN_ID
        await message.answer("❌ Anketa bekor qilindi.", reply_markup=admin_keyboard() if is_admin else main_menu())
        return

    await state.update_data(phone=message.text)
    data = await state.get_data()

    summary = (
        "📋 <b>Sizning ma'lumotlaringiz:</b>\n\n"
        f"💼 <b>Ish:</b> {data['job_type']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"🎓 <b>Ma'lumot:</b> {data['education']}\n"
        f"💼 <b>Avval ishlagan joy:</b> {data['previous_work']}\n"
        f"📚 <b>Hozirgi holat:</b> {data['current_status']}\n"
        f"📍 <b>Manzil:</b> {data['address']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        "Ma'lumotlar to'g'rimi?"
    )

    await message.answer_photo(photo=data['photo'], caption=summary, parse_mode="HTML", reply_markup=confirm_keyboard())


@router.callback_query(F.data == "confirm_send")
async def confirm_send(callback: CallbackQuery, state: FSMContext, bot):
    data = await state.get_data()
    user = callback.from_user
    database.save_user(user.id, data)

    username = user.username if user.username else "Yo'q"
    admin_message = (
        "📨 <b>Yangi anketa!</b>\n\n"
        f"💼 <b>Ish:</b> {data['job_type']}\n"
        f"👤 <b>Ism:</b> {data['name']}\n"
        f"🎂 <b>Yosh:</b> {data['age']}\n"
        f"🎓 <b>Ma'lumot:</b> {data['education']}\n"
        f"💼 <b>Avval ishlagan joy:</b> {data['previous_work']}\n"
        f"📚 <b>Hozirgi holat:</b> {data['current_status']}\n"
        f"📍 <b>Manzil:</b> {data['address']}\n"
        f"📞 <b>Telefon:</b> {data['phone']}\n\n"
        f"👨‍💼 <b>Username:</b> @{username}"
    )

    # Asosiy admin va super adminga yuborish
    for admin_id in [ADMIN_ID, SUPER_ADMIN_ID]:
        await bot.send_photo(
            chat_id=admin_id,
            photo=data['photo'],
            caption=admin_message,
            parse_mode="HTML",
            reply_markup=reply_to_user_keyboard(user.id)
        )

    user_id = callback.from_user.id
    is_admin = user_id in ALL_ADMINS
    await callback.message.answer("✅ Ma'lumotlaringiz muvaffaqiyatli yuborildi!\n\nTez orada siz bilan bog'lanamiz. 😊",
                                  reply_markup=admin_keyboard() if is_admin else main_menu())
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "restart_form")
async def restart_form(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(FormStates.job_type)
    await callback.message.answer("🔄 Anketani qayta to'ldiring.\n\nIshlamoqchi bo'lgan ishingiz:",
                                  reply_markup=job_types_keyboard())
    await callback.answer()


@router.message(F.text == "📢 Vakansiya e'lon qilish")
async def admin_vacancy(message: Message, state: FSMContext):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    await state.set_state(AdminStates.vacancy_text)
    await message.answer("📝 Yangi vakansiya matnini yuboring:\n\nBu matn barcha foydalanuvchilarga yuboriladi.",
                         reply_markup=cancel_keyboard())


@router.message(AdminStates.vacancy_text)
async def process_vacancy(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return

    # Vakansiyani saqlash
    await state.update_data(vacancy_text=message.text)

    # Tasdiqlash uchun ko'rsatish
    await message.answer(
        f"📋 <b>Vakansiya e'loni:</b>\n\n{message.text}\n\n"
        "E'lonni barcha foydalanuvchilarga yuborishni tasdiqlaysizmi?",
        parse_mode="HTML",
        reply_markup=vacancy_confirm_keyboard()
    )


@router.callback_query(F.data == "confirm_vacancy")
async def confirm_vacancy(callback: CallbackQuery, state: FSMContext, bot):
    """Vakansiyani tasdiqlash va yuborish"""
    data = await state.get_data()
    vacancy_text = data['vacancy_text']

    database.set_vacancy(vacancy_text)
    user_ids = database.get_all_user_ids()
    success_count = 0
    failed_count = 0

    await callback.message.answer("⏳ Yuborilmoqda...", reply_markup=admin_keyboard())

    for user_id in user_ids:
        if user_id == ADMIN_ID:
            continue
        try:
            await bot.send_message(chat_id=user_id, text=f"📢 <b>Yangi vakansiya e'loni!</b>\n\n{vacancy_text}",
                                   parse_mode="HTML")
            success_count += 1
        except Exception as e:
            failed_count += 1
            print(f"Failed to send to {user_id}: {e}")

    await callback.message.answer(
        f"✅ Vakansiya saqlandi!\n\n"
        f"📤 Muvaffaqiyatli: {success_count} ta\n"
        f"❌ Xatolik: {failed_count} ta\n"
        f"👥 Jami: {len(user_ids) - 1} ta foydalanuvchi",
        reply_markup=admin_keyboard()
    )
    await callback.answer()
    await state.clear()


@router.callback_query(F.data == "restart_vacancy")
async def restart_vacancy(callback: CallbackQuery, state: FSMContext):
    """Vakansiyani qayta yozish"""
    await state.set_state(AdminStates.vacancy_text)
    await callback.message.answer(
        "🔄 Vakansiya matnini qayta yozing:",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.message(F.text == "📊 Statistika")
async def admin_stats(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    users_count = database.get_users_count() - 1  # Admin hisoblanmasin
    all_users = database.get_all_users()
    applications_count = len(all_users)
    await message.answer(
        f"📊 <b>Statistika</b>\n\n👥 Jami foydalanuvchilar: {users_count}\n📝 Anketa yuborgan: {applications_count}",
        parse_mode="HTML", reply_markup=admin_keyboard())


@router.message(F.text == "🔍 Qidirish")
async def search_users_menu(message: Message):
    if message.from_user.id != ADMIN_ID:
        await message.answer("❌ Sizda ruxsat yo'q!")
        return
    await message.answer("🔍 <b>Qidiruv</b>\n\nQidiruv turini tanlang:", parse_mode="HTML",
                         reply_markup=search_filter_keyboard())


@router.callback_query(F.data.startswith("search_by_"))
async def search_filter_selected(callback: CallbackQuery, state: FSMContext):
    search_type = callback.data.split("_")[-1]
    search_names = {"name": "👤 Ism", "phone": "📞 Telefon", "address": "📍 Manzil", "work": "💼 Ish tajribasi"}
    await state.set_state(AdminStates.search_query)
    await state.update_data(search_type=search_type)
    await callback.message.answer(
        f"🔍 <b>{search_names[search_type]} bo'yicha qidirish</b>\n\nQidiruv so'zini kiriting:", parse_mode="HTML",
        reply_markup=cancel_keyboard())
    await callback.answer()


@router.callback_query(F.data == "cancel_search")
async def cancel_search(callback: CallbackQuery):
    await callback.message.answer("❌ Qidiruv bekor qilindi.", reply_markup=admin_keyboard())
    await callback.answer()


@router.message(AdminStates.search_query)
async def process_search_query(message: Message, state: FSMContext):
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Qidiruv bekor qilindi.", reply_markup=admin_keyboard())
        return

    query = message.text
    results = database.search_users(query)

    if not results:
        await message.answer(
            "❌ Hech narsa topilmadi.\n\nBoshqa so'z bilan qidiring yoki /admin buyrug'i bilan admin paneliga qayting.",
            reply_markup=cancel_keyboard())
        return

    response = "🔍 <b>Qidiruv natijalari:</b>\n\n"
    response += f"Topildi: {len(results)} ta\n\n"

    for i, (user_id, data) in enumerate(results[:10], 1):
        job_type = data.get('job_type', 'Noma\'lum')
        address = data.get('address', 'Noma\'lum')
        response += (
            f"{i}. 👤 <b>{data['name']}</b>\n"
            f"   💼 {job_type}\n"
            f"   📍 {address}\n"
            f"   📞 {data['phone']}\n"
            f"   💼 {data['work_experience']}\n"
            f"   🆔 ID: <code>{user_id}</code>\n\n"
        )

    if len(results) > 10:
        response += f"... va yana {len(results) - 10} ta natija"

    await message.answer(response, parse_mode="HTML", reply_markup=admin_keyboard())
    await state.clear()


# Eski contact_admin callback handleri o'chirildi - endi alohida "Murojaat qilish" tugmasi mavjud

@router.message(ContactStates.message)
async def process_contact_message(message: Message, state: FSMContext, bot):
    """Adminga xabar yuborish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=main_menu())
        return

    user = message.from_user
    username = user.username if user.username else "Yo'q"

    # Contact type ni olish
    data = await state.get_data()
    contact_type = data.get('contact_type', 'Murojaat')

    # Adminga xabar yuborish (javob tugmasi yo'q)
    admin_msg = (
        f"📨 <b>Yangi {contact_type.lower()}!</b>\n\n"
        f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
        f"👨‍💼 <b>Username:</b> @{username}\n\n"
        f"💬 <b>{contact_type}:</b>\n{message.text}"
    )

    try:
        # Asosiy admin va super adminga yuborish (javob tugmasi yo'q)
        for admin_id in [ADMIN_ID, SUPER_ADMIN_ID]:
            await bot.send_message(
                chat_id=admin_id,
                text=admin_msg,
                parse_mode="HTML"
            )

        # Foydalanuvchiga xabar
        response_msg = (
            f"✅ <b>{contact_type}ingiz uchun rahmat!</b>\n\n"
            f"Tez orada ko'rib chiqib, kerakli o'zgarishlarni amalga oshiramiz."
        )
        await message.answer(response_msg, parse_mode="HTML", reply_markup=main_menu())
    except Exception as e:
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
            reply_markup=main_menu()
        )
        print(f"Failed to send message to admin: {e}")

    await state.clear()


@router.callback_query(F.data.startswith("reply_"))
async def reply_button_clicked(callback: CallbackQuery, state: FSMContext):
    """Javob berish tugmasi bosildi"""
    user_id = int(callback.data.split("_")[1])
    await state.update_data(user_id=user_id)
    await state.set_state(ReplyStates.message)
    await callback.message.answer(
        f"💬 <b>Foydalanuvchiga javob berish</b>\n\n"
        f"Foydalanuvchi ID: {user_id}\n\n"
        "Javob xabaringizni yozing yoki rasm/video yuboring:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.message(ReplyStates.message)
async def process_reply_message(message: Message, state: FSMContext, bot):
    """Foydalanuvchiga javob yuborish - rasm, video, matn qo'llab-quvvatlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=admin_keyboard())
        return

    data = await state.get_data()
    user_id = data['user_id']

    try:
        # Rasm bilan javob
        if message.photo:
            sent_message = await bot.send_photo(
                chat_id=user_id,
                photo=message.photo[-1].file_id,
                caption=f"📩 <b>Admin javob berdi:</b>\n\n{message.caption or 'Rasm yuborildi'}",
                parse_mode="HTML",
                reply_markup=user_reply_keyboard()
            )
        # Video bilan javob
        elif message.video:
            sent_message = await bot.send_video(
                chat_id=user_id,
                video=message.video.file_id,
                caption=f"📩 <b>Admin javob berdi:</b>\n\n{message.caption or 'Video yuborildi'}",
                parse_mode="HTML",
                reply_markup=user_reply_keyboard()
            )
        # Matn javob
        elif message.text:
            sent_message = await bot.send_message(
                chat_id=user_id,
                text=f"📩 <b>Admin javob berdi:</b>\n\n{message.text}",
                parse_mode="HTML",
                reply_markup=user_reply_keyboard()
            )
        else:
            await message.answer("❌ Iltimos, matn, rasm yoki video yuboring!")
            return

        await message.answer(
            "✅ Javob muvaffaqiyatli yuborildi!",
            reply_markup=admin_keyboard()
        )
    except Exception as e:
        await message.answer(
            f"❌ Xatolik yuz berdi!\n\n"
            f"Foydalanuvchi topilmadi yoki botni bloklagan.\n\n"
            f"Xatolik: {str(e)}",
            reply_markup=admin_keyboard()
        )
        print(f"Failed to send reply to user {user_id}: {e}")

    await state.clear()


# Murojaat qilish handlerlari
@router.message(F.text == "📞 Murojaat qilish")
async def contact_menu(message: Message, bot, state: FSMContext):
    """Murojaat qilish menyusi"""
    # Avval state'ni tozalaymiz
    await state.clear()

    if not await subscription_required(message, bot):
        return

    await message.answer(
        "� <b>Murojaat qilish</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 Quyidagi variantlardan birini tanlang:\n\n"
        "💡 <i>Taklif</i> - Yaxshilash g'oyalari\n"
        "❓ <i>Savol</i> - Savollar va yordam",
        parse_mode="HTML",
        reply_markup=contact_options_keyboard()
    )


@router.callback_query(F.data == "contact_suggestion")
async def contact_suggestion(callback: CallbackQuery, state: FSMContext, bot):
    """Taklif yuborish"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(ContactStates.message)
    await state.update_data(contact_type="Taklif")
    await callback.message.answer(
        "💡 <b>Taklif yuborish</b>\n\n"
        "Taklifingizni yozing. Admin ko'rib chiqadi:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "contact_question")
async def contact_question(callback: CallbackQuery, state: FSMContext, bot):
    """Savol yuborish"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(ContactStates.message)
    await state.update_data(contact_type="Savol")
    await callback.message.answer(
        "❓ <b>Savol yuborish</b>\n\n"
        "Savolingizni yozing. Admin javob beradi:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "contact_complaint")
async def contact_complaint(callback: CallbackQuery, state: FSMContext, bot):
    """Shikoyat qilish - tur tanlash"""
    if not await subscription_required(callback, bot):
        return

    await callback.message.answer(
        "⚠️ <b>Shikoyat qilish</b>\n\n"
        "Shikoyat turini tanlang:",
        parse_mode="HTML",
        reply_markup=complaint_options_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "complaint_medicine")
async def complaint_medicine(callback: CallbackQuery, state: FSMContext, bot):
    """Dori yuzasidan shikoyat"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(ContactStates.message)
    await state.update_data(contact_type="Dori yuzasidan shikoyat")
    await callback.message.answer(
        "💊 <b>Dori yuzasidan shikoyat</b>\n\n"
        "Shikoyatingizni yozing. Admin ko'rib chiqadi:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "complaint_staff")
async def complaint_staff(callback: CallbackQuery, state: FSMContext, bot):
    """Xodim ustidan shikoyat"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(ContactStates.message)
    await state.update_data(contact_type="Xodim ustidan shikoyat")
    await callback.message.answer(
        "👤 <b>Xodim ustidan shikoyat</b>\n\n"
        "Shikoyatingizni yozing. Admin ko'rib chiqadi:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "check_subscription")
async def check_subscription_callback(callback: CallbackQuery, bot):
    """A'zolikni tekshirish tugmasi bosildi"""
    user_id = callback.from_user.id

    # Admin uchun a'zolik tekshiruvi yo'q
    if user_id == ADMIN_ID:
        await callback.message.answer("👋 Assalomu alaykum, Admin!\n\nSiz admin panelidasiz.",
                                      reply_markup=admin_keyboard())
        await callback.answer()
        return

    is_subscribed = await check_user_subscription(bot, user_id)

    if is_subscribed:
        vacancy_text = database.get_vacancy()
        await callback.message.answer(
            "✅ <b>Rahmat! Siz kanalga a'zo bo'ldingiz.</b>\n\n" + vacancy_text,
            parse_mode="HTML",
            reply_markup=main_menu()
        )
        await callback.answer("✅ A'zolik tasdiqlandi!")
    else:
        await callback.answer(
            "❌ Siz hali kanalga a'zo bo'lmadingiz!\n\nIltimos, avval kanalga a'zo bo'ling.",
            show_alert=True
        )


# Dori buyurtma handlerlari
@router.message(F.text == "💊 Dori buyurtma berish")
async def medicine_order_menu(message: Message, bot, state: FSMContext):
    """Dori buyurtma menyusi"""
    # Avval state'ni tozalaymiz
    await state.clear()

    if not await subscription_required(message, bot):
        return

    await message.answer(
        "💊 <b>Dori buyurtma</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 Quyidagi variantlardan birini tanlang:\n\n"
        "📋 <i>Retsepli</i> - Shifokor retsepti bilan\n"
        "💊 <i>Retsepsiz</i> - Oddiy dorilar\n"
        "⚗️ <i>Tayyorlanadigan</i> - Maxsus tayyorlanuvchi dorilar",
        parse_mode="HTML",
        reply_markup=medicine_order_keyboard()
    )


@router.callback_query(F.data == "medicine_medical_equipment")
async def medicine_medical_equipment(callback: CallbackQuery, state: FSMContext, bot):
    """Tibbiy buyum va texnikalar buyurtmasi"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(MedicineOrderStates.message)
    await state.update_data(order_type="Tibbiy buyum va texnikalar")
    await callback.message.answer(
        "🏥 <b>Tibbiy buyum va texnikalar buyurtmasi</b>\n\n"
        "Kerakli tibbiy buyum yoki texnika nomini yozing yoki rasmini yuboring.\n"
        "Miqdor va qo'shimcha ma'lumotlarni ham ko'rsating:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "medicine_prescription")
async def medicine_prescription(callback: CallbackQuery, state: FSMContext, bot):
    """Retsepli dori buyurtmasi"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(MedicineOrderStates.message)
    await state.update_data(order_type="Retsepli dori vositalari")
    await callback.message.answer(
        "📋 <b>Retsepli dori vositalari buyurtmasi</b>\n\n"
        "Retsept rasmini yoki dori nomini yuboring.\n"
        "Qo'shimcha ma'lumot ham yozishingiz mumkin:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "medicine_no_prescription")
async def medicine_no_prescription(callback: CallbackQuery, state: FSMContext, bot):
    """Retsepsiz dori buyurtmasi"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(MedicineOrderStates.message)
    await state.update_data(order_type="Retsepsiz dori vositalari")
    await callback.message.answer(
        "💊 <b>Retsepsiz dori vositalari buyurtmasi</b>\n\n"
        "Kerakli dori nomini yozing yoki rasmini yuboring.\n"
        "Miqdor va qo'shimcha ma'lumotlarni ham ko'rsating:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "medicine_custom")
async def medicine_custom(callback: CallbackQuery, state: FSMContext, bot):
    """Tayyorlanadigan dori buyurtmasi"""
    if not await subscription_required(callback, bot):
        return

    await state.set_state(MedicineOrderStates.message)
    await state.update_data(order_type="Tayyorlanadigan dori vositalari")
    await callback.message.answer(
        "⚗️ <b>Tayyorlanadigan dori vositalari buyurtmasi</b>\n\n"
        "Dori tarkibi, retsept yoki boshqa kerakli ma'lumotlarni yuboring.\n"
        "Rasm yoki matn ko'rinishida yuborishingiz mumkin:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.message(MedicineOrderStates.message)
async def process_medicine_order(message: Message, state: FSMContext, bot):
    """Dori buyurtmasini qayta ishlash"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=main_menu())
        return

    user = message.from_user
    username = user.username if user.username else "Yo'q"

    # Order type ni olish
    data = await state.get_data()
    order_type = data.get('order_type', 'Dori buyurtmasi')

    # Dori adminlariga xabar yuborish (MEDICINE_ADMIN va SUPER_ADMIN)
    admin_ids = [MEDICINE_ADMIN_ID, SUPER_ADMIN_ID]

    if message.photo:

        admin_msg = (
            f"💊 <b>Yangi {order_type.lower()}!</b>\n\n"
            f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
            f"👨‍💼 <b>Username:</b> @{username}\n\n"
            f"📝 <b>Izoh:</b>\n{message.caption or 'Rasm yuborildi'}"
        )

        try:
            # Har ikkala adminga yuborish
            for admin_id in admin_ids:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=message.photo[-1].file_id,
                    caption=admin_msg,
                    parse_mode="HTML",
                    reply_markup=reply_to_user_keyboard(user.id)
                )
            await message.answer(
                f"✅ {order_type} buyurtmangiz adminga yuborildi!\n\nTez orada javob beramiz.",
                reply_markup=main_menu()
            )
        except Exception as e:
            await message.answer(
                "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
                reply_markup=main_menu()
            )
            print(f"Failed to send medicine order to admin: {e}")

    elif message.text:
        # Matn xabar
        admin_msg = (
            f"💊 <b>Yangi {order_type.lower()}!</b>\n\n"
            f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
            f"👨‍💼 <b>Username:</b> @{username}\n\n"
            f"💬 <b>Buyurtma:</b>\n{message.text}"
        )

        try:
            # Har ikkala adminga yuborish
            for admin_id in admin_ids:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_msg,
                    parse_mode="HTML",
                    reply_markup=reply_to_user_keyboard(user.id)
                )
            await message.answer(
                f"✅ {order_type} buyurtmangiz adminga yuborildi!\n\nTez orada javob beramiz.",
                reply_markup=main_menu()
            )
        except Exception as e:
            await message.answer(
                "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
                reply_markup=main_menu()
            )
            print(f"Failed to send medicine order to admin: {e}")

    else:
        await message.answer(
            "❌ Iltimos, matn yoki rasm yuboring!",
            reply_markup=cancel_keyboard()
        )
        return

    await state.clear()


# Foydalanuvchi admin javobiga javob berish
@router.callback_query(F.data == "user_reply")
async def user_reply_button_clicked(callback: CallbackQuery, state: FSMContext):
    """Foydalanuvchi admin javobiga javob berish tugmasi bosildi"""
    await state.set_state(UserReplyStates.message)
    await state.update_data(admin_message_id=callback.message.message_id)

    await callback.message.answer(
        "💬 <b>Admin javobiga javob berish</b>\n\n"
        "Javobingizni yozing yoki rasm/video yuboring:",
        parse_mode="HTML",
        reply_markup=cancel_keyboard()
    )
    await callback.answer()


@router.message(UserReplyStates.message)
async def process_user_reply(message: Message, state: FSMContext, bot):
    """Foydalanuvchi admin javobiga javob yuborish"""
    if message.text == "❌ Bekor qilish":
        await state.clear()
        await message.answer("❌ Bekor qilindi.", reply_markup=main_menu())
        return

    user = message.from_user
    username = user.username if user.username else "Yo'q"

    try:
        # Rasm bilan javob
        if message.photo:
            admin_msg = (
                f"💬 <b>Foydalanuvchi javob berdi:</b>\n\n"
                f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
                f"👨‍💼 <b>Username:</b> @{username}\n\n"
                f"📝 <b>Javob:</b>\n{message.caption or 'Rasm yuborildi'}"
            )

            # Barcha adminlarga yuborish
            for admin_id in [ADMIN_ID, SUPER_ADMIN_ID]:
                await bot.send_photo(
                    chat_id=admin_id,
                    photo=message.photo[-1].file_id,
                    caption=admin_msg,
                    parse_mode="HTML",
                    reply_markup=reply_to_user_keyboard(user.id)
                )

        # Video bilan javob
        elif message.video:
            admin_msg = (
                f"💬 <b>Foydalanuvchi javob berdi:</b>\n\n"
                f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
                f"👨‍💼 <b>Username:</b> @{username}\n\n"
                f"📝 <b>Javob:</b>\n{message.caption or 'Video yuborildi'}"
            )

            # Barcha adminlarga yuborish
            for admin_id in [ADMIN_ID, SUPER_ADMIN_ID]:
                await bot.send_video(
                    chat_id=admin_id,
                    video=message.video.file_id,
                    caption=admin_msg,
                    parse_mode="HTML",
                    reply_markup=reply_to_user_keyboard(user.id)
                )

        # Matn javob
        elif message.text:
            admin_msg = (
                f"💬 <b>Foydalanuvchi javob berdi:</b>\n\n"
                f"👤 <b>Ism:</b> {user.first_name} {user.last_name or ''}\n"
                f"👨‍💼 <b>Username:</b> @{username}\n\n"
                f"💬 <b>Javob:</b>\n{message.text}"
            )

            # Barcha adminlarga yuborish
            for admin_id in [ADMIN_ID, SUPER_ADMIN_ID]:
                await bot.send_message(
                    chat_id=admin_id,
                    text=admin_msg,
                    parse_mode="HTML",
                    reply_markup=reply_to_user_keyboard(user.id)
                )

        else:
            await message.answer(
                "❌ Iltimos, matn, rasm yoki video yuboring!",
                reply_markup=cancel_keyboard()
            )
            return

        await message.answer(
            "✅ Javobingiz adminga yuborildi!",
            reply_markup=main_menu()
        )

    except Exception as e:
        await message.answer(
            "❌ Xatolik yuz berdi. Iltimos, keyinroq urinib ko'ring.",
            reply_markup=main_menu()
        )
        print(f"Failed to send user reply to admin: {e}")

    await state.clear()
