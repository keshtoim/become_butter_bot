"""Иконки для сообщений бота.

PNG лежат в assets/icons/png/ (собираются из вектора скриптом tools/build_icons.py).
Если файла нет — хелперы молча откатываются на обычный текст, бот не падает.
"""
from pathlib import Path

from aiogram import Bot
from aiogram.types import FSInputFile, Message

ICONS_DIR = Path(__file__).resolve().parent.parent / "assets" / "icons" / "png"


def get_icon(name: str) -> FSInputFile | None:
    path = ICONS_DIR / f"{name}.png"
    return FSInputFile(path) if path.exists() else None


def day_icon(day: int) -> str:
    return f"day_{day:02d}"


async def answer_with_icon(message: Message, icon_name: str, text: str, **kwargs) -> None:
    """Ответить картинкой с подписью, либо просто текстом, если иконки нет."""
    icon = get_icon(icon_name)
    if icon is not None:
        await message.answer_photo(icon, caption=text, **kwargs)
    else:
        await message.answer(text, **kwargs)


async def send_with_icon(bot: Bot, chat_id: int, icon_name: str, text: str, **kwargs) -> None:
    """То же самое, но для рассылки из планировщика."""
    icon = get_icon(icon_name)
    if icon is not None:
        await bot.send_photo(chat_id, icon, caption=text, **kwargs)
    else:
        await bot.send_message(chat_id, text, **kwargs)
