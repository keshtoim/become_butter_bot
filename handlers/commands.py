from aiogram import Router, types, F
from aiogram.filters import CommandStart
import database.requests as rq
from bot.keyboards import main_kb, get_task_kb
from data.content import TASKS
import random

router = Router()

# Ободряющие фразы для режима отдыха
ENCOURAGEMENT = [
    "Масло должно настояться. Отдыхай, завтра дадим жару! 🔥",
    "Даже самому элитному маслу нужен холод. Переведи дух. 🧊",
    "Не прогоркай! Отдых — это часть процесса. Жду тебя завтра. 💪",
    "Твоя текстура стабилизируется. Отдых — это тоже вклад в прогресс. ✨"
]


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    # Регистрация юзера
    await rq.set_user(message.from_user.id, message.from_user.username)

    await message.answer(
        "Йоу! Ты на связи с **Become Butter**. 🧈\n\n"
        "Твой путь от «сырых сливок» до «чистого золота» начинается здесь.\n"
        "Используй меню ниже, чтобы управлять своим прогрессом.",
        reply_markup=main_kb,
        parse_mode="Markdown"
    )


@router.message(F.text == "🧈 Мой профиль")
async def cmd_profile(message: types.Message):
    user = await rq.get_user(message.from_user.id)

    if not user:
        await message.answer("Сначала нажми /start!")
        return

    # Расчет прогресс-бара
    progress_percent = int((user.current_day / 28) * 100)
    filled_cells = int(user.current_day / 2.8)
    bar = "🧈" * filled_cells + "⬜" * (10 - filled_cells)

    await message.answer(
        f"👤 **ТВОЙ МАСЛЯНЫЙ ПРОФИЛЬ**\n\n"
        f"🏷 **Статус:** {user.status}\n"
        f"💧 **Butter Drops:** {user.butter_drops}\n"
        f"📅 **Прогресс:** {user.current_day}/28 дней\n"
        f"[{bar}] {progress_percent}%\n\n"
        f"Помни: чтобы всё шло как по маслу, нельзя пропускать задания! 🔥",
        reply_markup=main_kb,
        parse_mode="Markdown"
    )


@router.message(F.text == "🚀 Следующее задание")
async def cmd_next_task(message: types.Message):
    user = await rq.get_user(message.from_user.id)

    if user.current_day > 28:
        await message.answer("Ты уже достиг уровня **Solid Gold**! 🏆", parse_mode="Markdown")
        return

    task = TASKS.get(user.current_day)

    await message.answer(
        f"🔔 **ДЕНЬ {user.current_day}: {task['title']}**\n\n"
        f"{task['text']}\n\n"
        f"🔬 **Суть:** {task['science']}",
        reply_markup=get_task_kb(),
        parse_mode="Markdown"
    )


@router.message(F.text == "☕️ Взять отдых")
async def cmd_rest(message: types.Message):
    # Включаем режим отдыха в БД
    await rq.toggle_rest(message.from_user.id, True)

    phrase = random.choice(ENCOURAGEMENT)
    await message.answer(
        f"🛡 **Режим отдыха активирован**\n\n"
        f"{phrase}\n\n"
        f"Я не буду присылать задания 24 часа. Твой прогресс сохранен.",
        reply_markup=main_kb,
        parse_mode="Markdown"
    )