from aiogram import Router, types, F
from aiogram.filters import CommandStart
import database.requests as rq
from bot.keyboards import get_main_kb, get_task_kb
from bot.media import answer_with_icon, day_icon
from data.content import TASKS
import random

router = Router()

# Ободряющие фразы для тех, кто взял паузу
ENCOURAGEMENT = [
    "Масло должно настояться. Отдыхай, завтра дадим жару! 🔥",
    "Даже самому элитному маслу нужен холод. Переведи дух. 🧊",
    "Не прогоркай! Отдых — это часть процесса. Жду тебя завтра. 💪",
    "Твоя текстура стабилизируется. Отдых — это тоже вклад в прогресс. ✨"
]


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    user = await rq.get_user(message.from_user.id)

    await answer_with_icon(
        message,
        "action_start",
        "Йоу! Ты на связи с *Become Butter*. 🧈\n\n"
        "Твой путь от «сырых сливок» до «чистого золота» начинается здесь.\n"
        "Используй меню ниже, чтобы управлять своим прогрессом.",
        reply_markup=get_main_kb(user.is_resting),
        parse_mode="Markdown"
    )


@router.message(F.text == "🧈 Мой профиль")
async def cmd_profile(message: types.Message):
    user = await rq.get_user(message.from_user.id)

    # Расчет прогресс-бара
    progress_percent = int((user.current_day / 28) * 100)
    filled_cells = int(user.current_day / 2.8)
    bar = "🧈" * filled_cells + "⬜" * (10 - filled_cells)

    await answer_with_icon(
        message,
        "action_profile",
        f"👤 *ТВОЙ МАСЛЯНЫЙ ПРОФИЛЬ*\n\n"
        f"🏷 *Статус:* {user.status}\n"
        f"💧 *Butter Drops:* {user.butter_drops}\n"
        f"📅 *Прогресс:* {user.current_day}/28 дней\n"
        f"[{bar}] {progress_percent}%\n\n"
        f"Помни: чтобы всё шло как по маслу, нельзя пропускать задания! 🔥",
        reply_markup=get_main_kb(user.is_resting),
        parse_mode="Markdown"
    )


# Обработка кнопки задания (учитываем оба варианта текста)
@router.message(F.text.in_({"🚀 Следующее задание", "🔄 Вернуться к заданию"}))
async def cmd_next_task(message: types.Message):
    user = await rq.get_user(message.from_user.id)

    # Если юзер возвращается из отдыха, выключаем его в БД
    if user.is_resting:
        await rq.toggle_rest(user.tg_id, False)
        user.is_resting = False

    if user.current_day > 28:
        await answer_with_icon(message, "status_28_solid_gold",
                               "Ты уже достиг уровня *Solid Gold*! 🏆",
                               reply_markup=get_main_kb(False), parse_mode="Markdown")
        return

    task = TASKS.get(user.current_day)

    await answer_with_icon(
        message,
        day_icon(user.current_day),
        f"🔔 *ДЕНЬ {user.current_day}: {task['title']}*\n\n"
        f"{task['text']}\n\n"
        f"🔬 *Суть:* {task['science']}",
        reply_markup=get_task_kb(),
        parse_mode="Markdown"
    )


# Переключение режима отдыха
@router.message(F.text.in_({"☕️ Взять отдых", "☀️ Закончить отдых"}))
async def cmd_toggle_rest(message: types.Message):
    user = await rq.get_user(message.from_user.id)
    new_rest_state = not user.is_resting

    await rq.toggle_rest(message.from_user.id, new_rest_state)

    if new_rest_state:
        phrase = random.choice(ENCOURAGEMENT)
        text = f"🛡 *Режим отдыха активирован*\n\n{phrase}"
        icon = "action_rest_start"
    else:
        text = "☀️ *Режим отдыха выключен!*\nПора возвращаться к взбиванию твоей лучшей версии."
        icon = "action_rest_end"

    await answer_with_icon(message, icon, text,
                           reply_markup=get_main_kb(new_rest_state), parse_mode="Markdown")