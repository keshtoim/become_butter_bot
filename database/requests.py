from database.models import async_session, User
from sqlalchemy import select
from datetime import datetime
from sqlalchemy import select, update
import random

# Регистрация юзера (вызываем при /start)
async def set_user(tg_id, username):
    async with async_session() as session:
        # Проверка на наличие юзера в базе
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

# Получение данных юзера (для профиля и проверки статуса)
async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

# Обновление прогресса: день, капли и статус
async def update_user_progress(tg_id, new_day, new_drops, new_status):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(
                current_day=new_day,
                butter_drops=new_drops,
                status=new_status,
                last_task_sent=datetime.datetime.now()
            )
        )
        await session.commit()

# Получить всех пользователей для рассылки
async def get_all_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result.all()

# Переключение режима отдыха
async def toggle_rest(tg_id, status: bool):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(is_resting=status))
        await session.commit()

# Ободряющие фразы
ENCOURAGEMENT = [
    "Масло должно настояться. Отдыхай, завтра дадим жару! 🔥",
    "Даже самому элитному маслу нужен холод. Переведи дух. 🧊",
    "Не прогоркай! Отдых — это часть процесса. Жду тебя завтра. 💪"
]

def get_random_encouragement():
    return random.choice(ENCOURAGEMENT)