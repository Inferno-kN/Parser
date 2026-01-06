import asyncio
from aiogram import Bot, Dispatcher
from app.tg_bot.handlers.user_handlers import router as user_router
from config import TOKEN


async def main():
    bot = Bot(token=TOKEN)
    dp = Dispatcher()

    dp.include_router(user_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())