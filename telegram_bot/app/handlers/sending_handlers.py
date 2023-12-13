from aiogram import types, F
from aiogram.filters.command import Command

from app.bot import dp, bot
from services.main import full_search


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Парсер запущен")
    await full_search()
    await message.answer("Парсер остановлен")
