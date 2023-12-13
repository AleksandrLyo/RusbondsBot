import asyncio

from app.bot import run_polling


async def start():
    """Запуск бота."""
    await run_polling()


if __name__ == "__main__":
    asyncio.run(start())
