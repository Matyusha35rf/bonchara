from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


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


def sett() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Вкл/Выкл автопосещение", callback_data="toggle_autovisit")],
        [InlineKeyboardButton(text="🔔 Вкл/Выкл уведомления о следующей паре", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="🛎️ Вкл/Выкл уведомление о нажатии кнопки",
                              callback_data="toggle_button_notifications")],
        [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data="delete_account")]
    ])


def connect() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔑 Подключиться", callback_data="connect")]]
    )
