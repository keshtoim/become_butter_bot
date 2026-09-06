import os

from dotenv import load_dotenv

# Загружаем переменные из .env (если файл есть; на проде переменные обычно заданы в окружении)
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
# По умолчанию — локальный SQLite-файл рядом с проектом
DB_URL = os.getenv("DB_URL", "sqlite+aiosqlite:///database.db")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не задан. Скопируй .env.example в .env и впиши токен от @BotFather "
        "(или задай переменную окружения BOT_TOKEN на сервере)."
    )
