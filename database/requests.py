from database.models import async_session, User
from sqlalchemy import select

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