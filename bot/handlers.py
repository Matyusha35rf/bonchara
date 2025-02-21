import requests
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from database import save_to_db, toggle_availability, toggle_notifications, toggle_button_notifications, delete_account, \
    is_subscription_active
from keyboards import get_main_keyboard, get_profile_keyboard, get_back_to_profile_keyboard, \
    get_subscription_months_keyboard, get_settings_keyboard, get_connect_keyboard
from states import AuthStates
from av import auto_visit
from datetime import datetime, timedelta
import sqlite3


# Функция для регистрации всех обработчиков
def register_handlers(dp: Dispatcher):
    # Обработка команды /start
    @dp.message(Command("start"))
    async def start_command(message: types.Message):
        await message.answer("👋 Привет! Чтобы подключиться, нажмите кнопку ниже.", reply_markup=get_connect_keyboard())

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
            if auto_visit.System.auto(session, data['email'], message.text):
                save_to_db(data['user_id'], data['username'], data['email'], message.text)
                await message.answer("✅ Успешная авторизация!", reply_markup=get_main_keyboard())
            else:
                await message.answer("❌ Неверные данные. Попробуйте снова.")
            await state.clear()

    # 📄 Отображение профиля
    @dp.message(lambda m: m.text == "👤 Профиль")
    async def profile_message(message: types.Message):
        await show_profile(message, message.from_user.id)

    # Оформление подписки
    @dp.message(lambda m: m.text == "📝 Оформить подписку")
    async def subscription_message(message: types.Message):
        await message.answer("📅 Выберите количество месяцев подписки:", reply_markup=get_subscription_months_keyboard())
        await message.answer("🔙 Нажмите, чтобы вернуться в профиль:", reply_markup=get_back_to_profile_keyboard())

    @dp.callback_query(lambda c: c.data.startswith("subscribe_"))
    async def handle_subscription(callback: types.CallbackQuery):
        months = int(callback.data.split("_")[1])
        user_id = callback.from_user.id

        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()

        cursor.execute('SELECT sub_end_date FROM users WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()
        current_end_date = datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S') if result and result[0] else None

        now = datetime.now()
        if current_end_date and current_end_date > now:
            new_end_date = current_end_date + timedelta(days=30 * months)
        else:
            new_end_date = now + timedelta(days=30 * months)

        cursor.execute('''
            UPDATE users 
            SET sub = 1, sub_end_date = ?
            WHERE user_id = ?
        ''', (new_end_date.strftime('%Y-%m-%d %H:%M:%S'), user_id))

        conn.commit()
        conn.close()

        await callback.message.edit_text(f"✅ Подписка успешно продлена на {months} месяцев.")
        await show_profile(callback.message, user_id)
        await callback.answer()

    @dp.message(lambda m: m.text == "⚙️ Настройки")
    async def settings_message(message: types.Message):
        await message.answer("⚙️ Настройки:", reply_markup=get_settings_keyboard())
        await message.answer("🔽 Используйте кнопку ниже для возврата в главное меню", reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text="🔙 Назад")]],
            resize_keyboard=True
        ))

    # 🔙 Назад (возврат в главное меню)
    @dp.message(lambda m: m.text == "🔙 Назад")
    async def back_to_main(message: types.Message):
        await message.answer("🏠 Главное меню:", reply_markup=get_main_keyboard())

    @dp.callback_query(lambda c: c.data in ["toggle_autovisit", "toggle_notifications", "toggle_button_notifications"])
    async def toggle_callback(callback: types.CallbackQuery):
        user_id = callback.from_user.id

        if not is_subscription_active(user_id):
            await callback.answer("❌ У вас нет активной подписки.", show_alert=True)
            return

        if callback.data == "toggle_autovisit":
            state = toggle_availability(user_id)
            status = "🟢 Автопосещение включено!" if state else "🔴 Автопосещение выключено!"
        elif callback.data == "toggle_notifications":
            state = toggle_notifications(user_id)
            status = "🟢 Уведомления включены!" if state else "🔴 Уведомления выключены!"
        else:
            state = toggle_button_notifications(user_id)
            status = "🟢 Уведомления о нажатии кнопки включены!" if state else "🔴 Уведомления о нажатии кнопки выключены!"

        await callback.message.edit_text(status, reply_markup=get_settings_keyboard())
        await callback.answer()

    # 🗑️ Удаление аккаунта
    @dp.callback_query(lambda c: c.data == "delete_account")
    async def delete_account_callback(callback: types.CallbackQuery):
        delete_account(callback.from_user.id)
        await callback.message.answer("🗑️ Аккаунт удален. Хотите снова подключиться?",
                                      reply_markup=get_connect_keyboard())
        await callback.answer()


# Вспомогательная функция для отображения профиля
async def show_profile(message: types.Message, user_id: int):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username, sub, sub_end_date FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        username, sub, sub_end_date = user
        sub_status = "Активна" if sub else "Не активна"

        if sub and sub_end_date:
            end_date = datetime.strptime(sub_end_date, '%Y-%m-%d %H:%M:%S')
            remaining_days = (end_date - datetime.now()).days
            sub_info = f"📝 Подписка: {sub_status} ({remaining_days} дней)"
        else:
            sub_info = f"📝 Подписка: {sub_status}"

        await message.answer(
            f"👤 Ник: {username}\n{sub_info}",
            reply_markup=get_profile_keyboard()
        )
    else:
        await message.answer("❌ Профиль не найден.")
