import asyncio
import logging
from aiogram import Bot, Dispatcher

from config import TOKEN
from app.handlers import router
from app import database

bot = Bot(token=TOKEN)
dispatcher = Dispatcher()


async def on_startup(_):
    await database.create_database()
    print('BOT STARTED')


async def main():
    dispatcher.include_router(router)
    await dispatcher.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('BOT STOPPED')
