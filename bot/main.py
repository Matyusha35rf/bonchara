import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import register_handlers  # Импортируем функцию для регистрации обработчиков
import config


async def main():
    bot = Bot(token=config.api_token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)  # Создаем диспетчер

    # Регистрируем обработчики
    register_handlers(dp)

    # Инициализация базы данных
    from database import init_db
    init_db()

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
