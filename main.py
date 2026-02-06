import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(level=logging.INFO)


async def main():
    """Botni ishga tushirish"""
    bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()

    # Routerni ulash
    dp.include_router(router)

    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi!")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
