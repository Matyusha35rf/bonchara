import os

import requests

from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data import database

from bot import keyboards
from bot.states import AuthStates
from bot.until import check_and_remove_key

from datetime import datetime

from lk import lk_func, parsing_profile
from lk.update_subjects import update_subjects
from lk.parsing_profile import parsing_profile

from hashlib import md5


# Функция для регистрации всех обработчиков
def register_handlers(dp: Dispatcher):
    # Обработка команды /start
    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("👋 Привет! Чтобы подключиться, нажмите кнопку ниже.", reply_markup=keyboards.connect())

    # Подключение пользователя
    @dp.callback_query(lambda c: c.data == "connect")
    async def connect_callback(callback: types.CallbackQuery, state: FSMContext):
        await callback.message.answer("📧 Введите ваш email:")
        await state.set_state(AuthStates.waiting_for_email)
        await state.update_data(user_id=callback.from_user.id, username=callback.from_user.username)
        await callback.answer()

    @dp.message(AuthStates.waiting_for_email)
    async def process_email(message: types.Message, state: FSMContext):
        await state.update_data(email=message.text)
        await message.answer("🔒 Введите ваш пароль:")
        await state.set_state(AuthStates.waiting_for_password)

    @dp.message(AuthStates.waiting_for_password)
    async def process_password(message: types.Message, state: FSMContext):
        data = await state.get_data()
        with requests.Session() as session:
            if lk_func.auth(session, data['email'], message.text)[0]:
                prof = parsing_profile(session)
                update_subjects(session, prof['Семестр'], data['user_id'])
                database.add_to_db_reg(data['user_id'], data['username'], data['email'], message.text, prof['Группа'], prof['Семестр'])
                await message.answer("✅ Успешная авторизация!", reply_markup=keyboards.main())
            else:
                await message.answer("❌ Неверные данные. Попробуйте снова.", reply_markup=keyboards.connect())

            await state.clear()

    # 📄 Отображение профиля
    @dp.message(lambda m: m.text == "👤 Профиль" or m.text == "🔙 Назад в профиль")
    async def profile_message(message: types.Message):
        user = database.get_user(message.from_user.id)

        if user:
            username, sub, sub_end_date = user["username"], user["sub"], user["sub_end_date"]
            sub_status = "Активна" if sub else "Не активна"

            if sub and sub_end_date:
                end_date = datetime.strptime(sub_end_date, '%Y-%m-%d')
                remaining_days = (end_date - datetime.now()).days
                sub_info = f"📝 Подписка: {sub_status} ({remaining_days} дней)"
            else:
                sub_info = f"📝 Подписка: {sub_status}"

            await message.answer(
                f"👤 Ник: {username}\n{sub_info}",
                reply_markup=keyboards.profile()
            )
        else:
            await message.answer("❌ Профиль не найден.")

    # Оформление подписки
    @dp.message(lambda m: m.text == "📝 Оформить подписку")
    async def subscription_message(message: types.Message, state: FSMContext):
        await message.answer("📅 Введите ключ:", reply_markup=keyboards.back_to_profile())
        await state.set_state(AuthStates.waiting_for_key)

    @dp.message(AuthStates.waiting_for_key)
    async def handle_subscription(message: types.Message, state: FSMContext):
        if check_and_remove_key(os.path.join('keys.txt'), message.text):
            await message.answer("✅ Верный ключ\n")
            user_id = message.from_user.id
            database.sub(user_id, 1)
        else:
            await message.answer("❌ Неверный ключ")
        await profile_message(message)
        await state.clear()

    # настройки
    @dp.message(lambda m: m.text == "⚙️ Настройки")
    async def settings_message(message: types.Message):
        await message.answer("⚙️ Настройки:", reply_markup=keyboards.sett())
        await message.answer("🔽 Используйте кнопку ниже для возврата в главное меню", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔙 Назад")]],
            resize_keyboard=True
        ))

    # 🔙 Назад (возврат в главное меню)
    @dp.message(lambda m: m.text == "🔙 Назад")
    async def back_to_main(message: types.Message):
        await message.answer("🏠 Главное меню:", reply_markup=keyboards.main())

    @dp.callback_query(lambda c: c.data in ["toggle_notifications", "toggle_button_notifications"])
    async def toggle_callback(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        if not database.is_sub_activ(user_id):
            await callback.answer("❌ У вас нет активной подписки.", show_alert=True)
            return

        if callback.data == "toggle_notifications":
            state = database.sw_notif(user_id)
            status = "🟢 Уведомления включены!" if state else "🔴 Уведомления выключены!"
        else:
            state = database.sw_butt_notif(user_id)
            status = "🟢 Уведомления о нажатии кнопки включены!" if state else "🔴 Уведомления о нажатии кнопки выключены!"

        await callback.message.edit_text(status, reply_markup=keyboards.sett())
        await callback.answer()

    @dp.callback_query(lambda c: c.data.startswith("av_"))
    async def handle_av_actions(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        action = callback.data  # "av_settings", "av_sw" и т.д.

        # Проверка подписки
        if not database.is_sub_activ(user_id):
            await callback.answer("❌ Требуется активная подписка", show_alert=True)
            return

        # Обработка переключения статуса
        if action == "av_sw":
            new_status = database.sw_av(user_id)
            status_text = "🟢 Включено" if new_status else "🔴 Выключено"
            await callback.answer(f"Статус изменён: {status_text}")

        # Обновляем сообщение для ЛЮБОГО действия
        current_status = database.get_user(user_id)['av_status']
        status_display = "🟢 Включено" if current_status else "🔴 Выключено"

        await callback.message.edit_text(
            f"🤖 Настройки автопосещения\nТекущий статус: {status_display}",
            reply_markup=keyboards.av_settings()
        )

    # Настройки предметов
    @dp.callback_query(lambda c: c.data == "subject_settings")
    async def subject_settings_callback(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        if not database.is_sub_activ(user_id):
            await callback.answer("❌ У вас нет активной подписки.", show_alert=True)
            return

        subjects = database.get_subjects_status(user_id)
        await callback.message.edit_text(
            "📚 Настройки предметов\nВыберите предметы для автопосещения:",
            reply_markup=keyboards.subject_settings_keyboard(subjects)
        )
        await callback.answer()

    # Обновление списка предметов
    @dp.callback_query(lambda c: c.data == "refresh_subjects")
    async def refresh_subjects_callback(callback: types.CallbackQuery):
        user_id = callback.from_user.id
        user = database.get_user(user_id)
        with requests.Session() as session:
            if lk_func.auth(session, user['email'], user['password'])[0]:
                prof = parsing_profile(session)
                update_subjects(session, prof['Семестр'], user_id)
                subjects = database.get_subjects_status(user_id)
                await callback.message.edit_text(
                    "🔄 Список предметов обновлен:",
                    reply_markup=keyboards.subject_settings_keyboard(subjects)
                )
        await callback.answer()

    # Обработчик для переключения статуса предмета
    @dp.callback_query(lambda c: c.data.startswith("subj_"))
    async def subject_toggle_callback(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        subject_hash = callback.data.replace("subj_", "")
        data = await state.get_data()

        # Получаем предмет по хешу
        subjects = database.get_subjects_status(user_id)
        selected_subject = next(
            (subj for subj in subjects
             if md5(subj.encode()).hexdigest()[:8] == subject_hash),
            None
        )

        if not selected_subject:
            await callback.answer("❌ Предмет не найден")
            return

        # Режим удаления
        if data.get('is_deletion_mode', False):
            selected_subjects = data.get('selected_subjects', [])

            if selected_subject in selected_subjects:
                selected_subjects.remove(selected_subject)
            else:
                selected_subjects.append(selected_subject)

            await state.update_data(selected_subjects=selected_subjects)
            await callback.message.edit_reply_markup(
                reply_markup=keyboards.subject_settings_keyboard(
                    subjects,
                    selected_subjects,
                    True
                )
            )
        # Обычный режим (переключение статуса)
        else:
            new_status = database.sw_subject_status(user_id, selected_subject)
            await callback.message.edit_reply_markup(
                reply_markup=keyboards.subject_settings_keyboard(
                    database.get_subjects_status(user_id)
                )
            )
            await callback.answer(
                f"Статус изменён: {'🟢 Вкл' if new_status else '🔴 Выкл'}"
            )

    # Режим удаления предметов
    @dp.callback_query(lambda c: c.data == "delete_nonexistent")
    async def delete_nonexistent_callback(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        subjects = database.get_subjects_status(user_id)
        await state.update_data(selected_subjects=[], is_deletion_mode=True)
        await callback.message.edit_text(
            "🗑️ Выберите предметы для удаления:",
            reply_markup=keyboards.subject_settings_keyboard(subjects, [], True)
        )
        await callback.answer()

    # Обработчик для режима удаления предметов
    @dp.callback_query(lambda c: c.data.startswith("subject_"))
    async def subject_deletion_callback(callback: types.CallbackQuery, state: FSMContext):
        subject = callback.data.replace("subject_", "")
        data = await state.get_data()

        if not data.get('is_deletion_mode', False):
            await callback.answer("❌ Неверный режим")
            return

        selected_subjects = data.get('selected_subjects', [])
        if subject in selected_subjects:
            selected_subjects.remove(subject)
        else:
            selected_subjects.append(subject)

        await state.update_data(selected_subjects=selected_subjects)

        # Обновляем клавиатуру
        user_id = callback.from_user.id
        subjects = database.get_subjects_status(user_id)
        await callback.message.edit_reply_markup(
            reply_markup=keyboards.subject_settings_keyboard(subjects, selected_subjects, True)
        )
        await callback.answer()

    # Подтверждение удаления
    @dp.callback_query(lambda c: c.data == "confirm_deletion")
    async def confirm_deletion_callback(callback: types.CallbackQuery, state: FSMContext):
        data = await state.get_data()
        selected_subjects = data.get('selected_subjects', [])
        subjects = database.get_subjects_status(user_id=callback.from_user.id)
        if selected_subjects:
            database.del_subjects(callback.from_user.id, selected_subjects)
            subjects = database.get_subjects_status(user_id=callback.from_user.id)
            await callback.message.edit_text(
                f"✅ Удалено {len(selected_subjects)} предметов",
                reply_markup=keyboards.subject_settings_keyboard(subjects)
            )
        else:
            await callback.message.edit_text(
                "❌ Не выбрано ни одного предмета для удаления",
                reply_markup=keyboards.subject_settings_keyboard(subjects)
            )

        await state.clear()
        await callback.answer()

    # Кнопки назад
    @dp.callback_query(lambda c: c.data == "back_to_autovisit")
    async def back_to_autovisit_callback(callback: types.CallbackQuery, state: FSMContext):
        user_id = callback.from_user.id
        await state.clear()
        current_status = database.get_user(user_id)["av_status"]
        status_text = "🟢 Включено" if current_status else "🔴 Выключено"

        # Формируем сообщение с текущим статусом
        message_text = f"🤖 Настройки автопосещения\nТекущий статус: {status_text}"
        await callback.message.edit_text(message_text, reply_markup=keyboards.av_settings())

    @dp.callback_query(lambda c: c.data == "back_to_settings")
    async def back_to_settings_callback(callback: types.CallbackQuery, state: FSMContext):
        await state.clear()
        await callback.message.edit_text("⚙️ Настройки:", reply_markup=keyboards.sett())
        await callback.answer()

    # Удаление аккаунта
    @dp.callback_query(lambda c: c.data == "delete_account")
    async def delete_account_callback(callback: types.CallbackQuery):
        database.del_acc(callback.from_user.id)
        await callback.message.answer("🗑️ Аккаунт удален. Хотите снова подключиться?",
                                      reply_markup=keyboards.connect())
        await callback.answer()
