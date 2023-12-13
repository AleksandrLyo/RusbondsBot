import logging
from aiogram import Bot, Dispatcher

from core.config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.token)
dp = Dispatcher()


async def run_polling():
    await dp.start_polling(bot)