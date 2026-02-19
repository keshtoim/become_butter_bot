from database.models import async_session, User
from sqlalchemy import select, update
import datetime # Импортируем весь модуль, так надежнее

# Регистрация юзера
async def set_user(tg_id, username):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

# Получение данных юзера
async def get_user(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id == tg_id))

# Обновление прогресса (то, где была ошибка)
async def update_user_progress(tg_id, new_day, new_drops, new_status):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(
                current_day=new_day,
                butter_drops=new_drops,
                status=new_status,
                last_task_sent=datetime.datetime.now() # Исправлено здесь
            )
        )
        await session.commit()

# Включение/выключение режима отдыха
async def toggle_rest(tg_id, status: bool):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(is_resting=status)
        )
        await session.commit()

# Получение всех юзеров для рассылки (нужно для планировщика)
async def get_all_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result.all()