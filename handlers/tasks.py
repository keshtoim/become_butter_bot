from aiogram import Router, F, types
from aiogram.types import CallbackQuery
import database.requests as rq
from data.content import STATUSES

router = Router()


# Обработка кнопки "Сделано!" ✅
@router.callback_query(F.data == "task_done")
async def task_done_handler(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)

    # Защита от багов (если юзера нет в базе)
    if not user:
        await callback.answer("Ошибка: юзер не найден.")
        return

    # Логика завершения марафона
    if user.current_day >= 28:
        await callback.message.edit_reply_markup(reply_markup=None)
        await callback.message.answer(
            "🏆 **УРОВЕНЬ SOLID GOLD ДОСТИГНУТ!**\n\n"
            "Ты прошел путь трансформации до конца. Твое масло теперь высшей пробы. "
            "Гордись собой, легенда!",
            parse_mode="Markdown"
        )
        await callback.answer()
        return

    # Расчет новых показателей
    new_day = user.current_day + 1
    new_drops = user.butter_drops + 10

    # Определяем статус (проверяем пороги из STATUSES)
    current_status = user.status
    for day_threshold in sorted(STATUSES.keys()):
        if new_day >= day_threshold:
            current_status = STATUSES[day_threshold]

    # Сохраняем прогресс в БД
    await rq.update_user_progress(callback.from_user.id, new_day, new_drops, current_status)

    # Убираем кнопки у сообщения, чтобы нельзя было нажать еще раз
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        f"✅ **Задание выполнено!**\n\n"
        f"💧 Начислено: +10 капель масла.\n"
        f"📅 Прогресс: {new_day}/28 дней.\n"
        f"🏷 Новый статус: {current_status}",
        parse_mode="Markdown"
    )

    await callback.answer("Красава!")


# Обработка кнопки "Не вышло" ❌
@router.callback_query(F.data == "task_failed")
async def task_failed_handler(callback: CallbackQuery):
    # Убираем кнопки, чтобы сообщение стало архивным
    await callback.message.edit_reply_markup(reply_markup=None)

    await callback.message.answer(
        "Ничего страшного! 🥣\n"
        "Масло не всегда взбивается с первого раза. Иногда нужно просто дать ему остыть.\n\n"
        "Попробуй выполнить задание завтра или используй кнопку **☕️ Взять отдых**, если чувствуешь, что перегораешь.",
        parse_mode="Markdown"
    )

    await callback.answer("Принято, не сдавайся!")