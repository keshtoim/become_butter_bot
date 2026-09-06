from aiogram import Router, F, types
from aiogram.types import CallbackQuery
import database.requests as rq
from data.content import STATUSES, STATUS_ICONS
from bot.keyboards import get_main_kb
from bot.media import answer_with_icon

router = Router()


@router.callback_query(F.data == "task_done")
async def task_done_handler(callback: CallbackQuery):
    user = await rq.get_user(callback.from_user.id)

    if not user:
        await callback.answer("Ошибка: юзер не найден.")
        return

    if user.current_day >= 28:
        await callback.message.edit_reply_markup(reply_markup=None)
        await answer_with_icon(callback.message, "status_28_solid_gold",
                               "🏆 *SOLID GOLD!* Ты прошел весь путь!", parse_mode="Markdown")
        await callback.answer()
        return

    # Прогресс
    new_day = user.current_day + 1
    new_drops = user.butter_drops + 10

    # Автоматическая смена статуса
    current_status = user.status
    reached_threshold = None
    for day_threshold in sorted(STATUSES.keys()):
        if new_day >= day_threshold:
            current_status = STATUSES[day_threshold]
            if new_day == day_threshold:
                reached_threshold = day_threshold

    await rq.update_user_progress(callback.from_user.id, new_day, new_drops, current_status)

    await callback.message.edit_reply_markup(reply_markup=None)

    # На днях смены статуса (7/14/21/28) показываем иконку нового статуса, иначе — «сделано»
    icon_name = STATUS_ICONS.get(reached_threshold, "action_done")

    await answer_with_icon(
        callback.message,
        icon_name,
        f"✅ *Задание выполнено!*\n\n"
        f"💧 Начислено: +10 капель масла.\n"
        f"📅 Прогресс: {new_day}/28 дней.\n"
        f"🏷 Статус: {current_status}",
        reply_markup=get_main_kb(False),  # Гарантируем стандартную клаву
        parse_mode="Markdown"
    )

    await callback.answer("Так держать!")


@router.callback_query(F.data == "task_failed")
async def task_failed_handler(callback: CallbackQuery):
    await callback.message.edit_reply_markup(reply_markup=None)

    await answer_with_icon(
        callback.message,
        "action_failed",
        "Ничего страшного! 🥣\n"
        "Попробуй выполнить задание позже или возьми отдых, чтобы восстановить ресурсы.",
        reply_markup=get_main_kb(False),
        parse_mode="Markdown"
    )

    await callback.answer("Главное — не сдаваться!")