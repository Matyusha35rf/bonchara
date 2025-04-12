from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from hashlib import md5

def connect() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔑 Подключиться", callback_data="connect")]]
    )


def main() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )


def profile() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="📝 Оформить подписку")]
        ],
        resize_keyboard=True
    )


def back_to_profile() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад в профиль")]],
        resize_keyboard=True
    )


def sett():
    buttons = [
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="🔄 Уведомления о нажатии кнопки", callback_data="toggle_button_notifications")],
        [InlineKeyboardButton(text="🤖 Настройки автопосещения", callback_data="av_setting")],
        [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data="delete_account")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def av_settings():
    buttons = [
        [InlineKeyboardButton(text="🔄 Вкл/Выкл автопосещение", callback_data="av_sw")],
        [InlineKeyboardButton(text="📝 Настроить список предметов", callback_data="subject_settings")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_settings")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def subject_settings_keyboard(subjects, selected_subjects=None, is_deletion_mode=False):
    if selected_subjects is None:
        selected_subjects = []

    buttons = []
    for subject, status in subjects.items():
        # Генерируем уникальный хеш для каждого предмета (8 символов)
        subject_hash = md5(subject.encode()).hexdigest()[:8]

        if is_deletion_mode:
            prefix = "✅" if subject in selected_subjects else ""
            text = f"{prefix} {subject}"
        else:
            status_icon = "🟢" if status else "🔴"
            text = f"{status_icon} {subject}"
        buttons.append([InlineKeyboardButton(text=text, callback_data=f"subj_{subject_hash}")])

    if is_deletion_mode:
        buttons.append([InlineKeyboardButton(text="✔️ Подтвердить выбор", callback_data="confirm_deletion")])
    else:
        buttons.append([InlineKeyboardButton(text="🔄 Обновить список предметов", callback_data="refresh_subjects")])
        buttons.append(
            [InlineKeyboardButton(text="🗑️ Удалить несуществующие дисциплины", callback_data="delete_nonexistent")])

    buttons.append([InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_autovisit")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
