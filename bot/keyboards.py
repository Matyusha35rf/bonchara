from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👤 Профиль")],
            [KeyboardButton(text="⚙️ Настройки")]
        ],
        resize_keyboard=True
    )


def get_profile_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="📝 Оформить подписку")]
        ],
        resize_keyboard=True
    )


def get_back_to_profile_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )


def get_subscription_months_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="1 месяц", callback_data="subscribe_1"),
             InlineKeyboardButton(text="3 месяца", callback_data="subscribe_3"),
             InlineKeyboardButton(text="6 месяцев", callback_data="subscribe_6")]
        ]
    )


def get_settings_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Вкл/Выкл автопосещение", callback_data="toggle_autovisit")],
        [InlineKeyboardButton(text="🔔 Вкл/Выкл уведомления о следующей паре", callback_data="toggle_notifications")],
        [InlineKeyboardButton(text="🛎️ Вкл/Выкл уведомление о нажатии кнопки",
                              callback_data="toggle_button_notifications")],
        [InlineKeyboardButton(text="🗑️ Удалить аккаунт", callback_data="delete_account")]
    ])


def get_connect_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="🔑 Подключиться", callback_data="connect")]]
    )
