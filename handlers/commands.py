from aiogram import Router, types
from aiogram.filters import CommandStart
import database.requests as rq

router = Router()


@router.message(CommandStart())
async def cmd_start(message: types.Message):
    # Регистрируем юзера в базе
    await rq.set_user(message.from_user.id, message.from_user.username)

    await message.answer(
        "Йоу! Ты на связи с Become Butter. 🧈\n\n"
        "Ты здесь, чтобы превратиться из «жидких сливок» в «чистое золото».\n"
        "Каждый день я буду присылать тебе задания, которые сделают твою жизнь Smooth.\n\n"
        "Твой текущий статус: 🥛 Raw Cream.\n"
        "Жди первое задание завтра утром!"
    )