from sqlalchemy import BigInteger, String, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from bot.config import DB_URL

# Создаем асинхронный движок
engine = create_async_engine(url=DB_URL)
# Фабрика сессий для работы с БД
async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str] = mapped_column(String(50), nullable=True)

    # Статистика игрока
    current_day: Mapped[int] = mapped_column(Integer, default=1)
    butter_drops: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(30), default="Raw Cream 🥛")

    # Таймштампы
    last_task_sent = mapped_column(DateTime, server_default=func.now())
    joined_at = mapped_column(DateTime, server_default=func.now())

# Инициализация таблиц
async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)