from aiogram import Router, F, types
from aiogram.types import CallbackQuery
import database.requests as rq
from data.content import STATUSES

router = Router()


# Обработка кнопки "Сделано!"
@router.callback_query(F.data == "task_done")
async def task_done_handler(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)

    # Расчет новых показателей
    new_day = user.current_day + 1
    new_drops = user.butter_drops + 10  # Даем 10 капель за задание

    # Определяем статус на основе мапы из content.py
    # Берем самый подходящий статус (ближайший меньший или равный текущему дню)
    current_status = user.status
    for day_milestone, status_name in STATUSES.items():
        if new_day >= day_milestone:
            current_status = status_name

    # Если марафон закончен (28 дней)
    if user.current_day >= 28:
        await callback.message.answer("Поздравляю! Ты прошел путь Solid Gold! 🏆\nТвое масло теперь высшей пробы.")
        await callback.answer()
        return

    # Обновляем данные в БД
    await rq.update_user_progress(callback.from_user.id, new_day, new_drops, current_status)

    # Убираем кнопку у старого сообщения, чтобы не кликали дважды
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        f"Отлично сработано! +10 капель масла 💧\n"
        f"Твой текущий прогресс: {new_day}/28 дней.\n"
        f"Твой статус: {current_status}"
    )

    # Обязательно отвечаем на колбэк, чтобы убрать "часики" в телеграме
    await callback.answer("Задание принято!")