from database.models import async_session
from database.models import User
from sqlalchemy import select

# Регистрация пользователя, если его нет в базе
async def set_user(tg_id, username):
    async with async_session() as session:
        # Проверяем наличие юзера в БД
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id, username=username))
            await session.commit()