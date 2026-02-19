from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.content import TASKS
import database.requests as rq
from datetime import datetime, timedelta


async def send_daily_task(bot: Bot):
    users = await rq.get_all_users()
    for user in users:
        if user.is_resting:
            # Если юзер отдыхал — снимаем режим отдыха и шлем ободрение
            await rq.toggle_rest(user.tg_id, False)
            await bot.send_message(user.tg_id, "Ты отдохнул? Пора возвращаться в форму! 🧈")
            continue

# Функция, которая будет запускаться по расписанию
async def send_daily_task(bot: Bot):
    users = await rq.get_all_users()

    for user in users:
        # Проверяем, прошло ли 24 часа с последней отправки
        if datetime.now() - user.last_task_sent >= timedelta(hours=24):
            # Если марафон еще не закончен
            if user.current_day <= 28:
                task = TASKS[user.current_day]

                # Формируем кнопку подтверждения
                keyboard = InlineKeyboardMarkup(inline_keyboard=[
                    [InlineKeyboardButton(text="Сделано! ✅", callback_data="task_done")]
                ])

                # Красиво оформляем текст задания
                message_text = (
                    f"🔔 **ДЕНЬ {user.current_day}: {task['title']}**\n\n"
                    f"{task['text']}\n\n"
                    f"🔬 **Суть:** {task['science']}"
                )

                try:
                    await bot.send_message(user.tg_id, message_text, reply_markup=keyboard, parse_mode="Markdown")
                    # ВАЖНО: Мы не обновляем день здесь. День обновится, когда юзер нажмет "Сделано" в tasks.py
                except Exception as e:
                    print(f"Ошибка при отправке пользователю {user.tg_id}: {e}")


# Инициализация планировщика
def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler()
    # Проверка базы каждый час
    scheduler.add_job(send_daily_task, "interval", hours=1, args=[bot])
    scheduler.start()


