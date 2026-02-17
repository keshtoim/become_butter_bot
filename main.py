import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from database.models import async_main

async def main():
    # Создаем таблицы при старте
    await async_main()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    # Включаем логирование
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот ушел в оффлайн')

