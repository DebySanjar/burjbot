import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiohttp import ClientTimeout

from config import BOT_TOKEN
from handlers import router

logging.basicConfig(level=logging.INFO)

async def main():
    """Botni ishga tushirish"""
    # Timeout sozlamalari
    timeout = ClientTimeout(total=30, connect=10)
    
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()
    
    # Routerni ulash
    dp.include_router(router)
    
    # Botni ishga tushirish
    print("🤖 Bot ishga tushdi!")
    try:
        await dp.start_polling(bot)
    except Exception as e:
        print(f"❌ Xatolik: {e}")
        print("🔄 5 soniyadan keyin qayta urinib ko'ramiz...")
        await asyncio.sleep(5)
        await main()  # Qayta ishga tushirish

if __name__ == "__main__":
    asyncio.run(main())
