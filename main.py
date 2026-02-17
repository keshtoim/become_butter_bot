import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from bot.config import BOT_TOKEN
from database.models import async_main
from handlers import commands
from handlers.tasks import router as task_router


async def main():
    # Создаем таблицы при старте
    await async_main()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(task_router)

    # Включаем логирование
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    # Запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот ушел в оффлайн')

