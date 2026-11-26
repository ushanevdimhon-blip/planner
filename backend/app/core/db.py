from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

# Naming convention для автоматической генерации имён FK, индексов и т.д.
convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    metadata = MetaData(naming_convention=convention)


# Создаем асинхронный движок
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,  # Пока True для отладки
)

# Фабрика асинхронных сессий
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db():
    """Зависимость FastAPI для получения асинхронной сессии БД."""
    async with SessionLocal() as session:
        yield session