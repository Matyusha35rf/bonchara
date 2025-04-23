import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.handlers import register_handlers  # Импортируем функцию для регистрации обработчиков
import config


bot = Bot(token=config.api_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # Создаем диспетчер


async def main():
    # Регистрируем обработчики
    register_handlers(dp)

    # Инициализация базы данных
    from data.database import init_db
    init_db()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
