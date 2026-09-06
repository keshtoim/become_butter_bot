import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.config import BOT_TOKEN
from database.models import async_main
from handlers import commands
from handlers.tasks import router as task_router
from services.scheduler import setup_scheduler

logging.basicConfig(
    level=logging.INFO,
    stream=sys.stdout,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


async def main():
    # Создаем таблицы при старте
    await async_main()

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()

    # Регистрируем роутеры
    dp.include_router(commands.router)
    dp.include_router(task_router)

    # Запуск планировщика рассылки
    setup_scheduler(bot)

    try:
        # Сбрасываем накопившиеся апдейты, чтобы бот не отвечал на старые сообщения после простоя
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Бот ушел в оффлайн")
