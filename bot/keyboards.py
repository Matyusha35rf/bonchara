from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from hashlib import md5


def connect() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔑 Подключиться", callback_data="connect"),
                InlineKeyboardButton(text="🧪 Тест-режим", callback_data="test_mode")
            ]
        ]
    )


def yes_no_recon() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Да", callback_data="delete_acc"),
         InlineKeyboardButton(text="Нет", callback_data="main")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def main() -> ReplyKeyboardMarkup:
    buttons = [
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="🗓 Расписание"), KeyboardButton(text="⚙️ Настройки")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def schedule_type() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="📅 Сегодня"), KeyboardButton(text="➡️ Завтра")],
        [KeyboardButton(text="7️⃣ Эта неделя"), KeyboardButton(text="➡️ След неделя")],
        [KeyboardButton(text="🔙 В главное меню")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def profile() -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text="🔙 В главное меню"), KeyboardButton(text="📝 Оформить подписку")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def sett():
    buttons = [
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="🔄 Уведомления о нажатии кнопки", callback_data="toggle_button_notifications")],
        [InlineKeyboardButton(text="🤖 Настройки автопосещения", callback_data="av_setting")],
        [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data="delete_acc")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def av_settings():
    buttons = [
        [InlineKeyboardButton(text="🔄 Вкл/Выкл автопосещение", callback_data="av_sw")],
        [InlineKeyboardButton(text="📝 Настроить автопосещение по предметам", callback_data="subject_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subject_settings_keyboard(subjects):
    buttons = []
    for subject, status in subjects.items():
        # Генерируем уникальный хеш для каждого предмета (8 символов)
        subject_hash = md5(subject.encode()).hexdigest()[:8]

        status_icon = "🟢" if status else "🔴"
        text = f"{status_icon} {subject}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"subj_{subject_hash}")])

    buttons.append([InlineKeyboardButton(text="🔄 Обновить предметы", callback_data="refresh_subjects")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_autovisit")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
