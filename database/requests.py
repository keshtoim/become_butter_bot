from database.models import async_session, engine, User, Base
from sqlalchemy import select, update
import datetime

# Database engine initialization
async def db_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all())

# User registration logic
async def set_user(tg_id, username=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()

# Progress and status update
async def update_user_day(tg_id, new_day: int, new_status: str):
    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == tg_id)
            .values(current_day=new_day, status=new_status, last_task_sent=datetime.datetime.now())
        )
        await session.commit()

# Award drops for task completion
async def add_butter_drops(tg_id, amount: int):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if user:
            user.butter_drops += amount
            await session.commit()