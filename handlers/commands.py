from aiogram import Router, types
from aiogram.filters import CommandStart, Command
import database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    await rq.set_user(message.from_user.id, message.from_user.username)
    await message.answer(
        "Йоу! Ты на связи с Become Butter. 🧈\n\n"
        "Твой путь от «сырых сливок» до «чистого золота» начинается здесь.\n"
        "Каждые 24 часа ты будешь получать новое задание.\n\n"
        "Твой текущий статус: 🥛 Raw Cream.\n"
        "Используй /profile, чтобы следить за прогрессом!"
    )


@router.message(Command("profile"))
async def cmd_profile(message: types.Message):
    user = await rq.get_user(message.from_user.id)

    if not user:
        await message.answer("Сначала нажми /start, чтобы я тебя запомнил!")
        return

    # Рисуем простой прогресс-бар (10 сегментов)
    progress_percent = (user.current_day / 28) * 100
    filled_cells = int(user.current_day / 2.8)  # 28 дней / 10 сегментов = 2.8
    bar = "🧈" * filled_cells + "⬜" * (10 - filled_cells)

    await message.answer(
        f"👤 **ТВОЙ МАСЛЯНЫЙ ПРОФИЛЬ**\n\n"
        f"🏷 Статус: {user.status}\n"
        f"💧 Butter Drops: {user.butter_drops}\n"
        f"📅 Прогресс: {user.current_day}/28 дней\n"
        f"[{bar}] {int(progress_percent)}%\n\n"
        f"Помни: чтобы всё шло как по маслу, нельзя пропускать задания! 🔥"
    )