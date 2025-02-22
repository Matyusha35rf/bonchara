from aiogram.fsm.state import StatesGroup, State


class AuthStates(StatesGroup):
    waiting_for_email = State()
    waiting_for_password = State()
    waiting_for_key = State()
