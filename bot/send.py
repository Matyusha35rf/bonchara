import asyncio

from bot.main import bot


async def send_message_async(chat_id: int, text: str):
    await bot.send_message(chat_id, text)

def send_message(chat_id, text):
    asyncio.run(send_message_async(chat_id,text))
