from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

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

class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass

async def get_db():
    """Зависимость FastAPI для получения асинхронной сессии БД."""
    async with SessionLocal() as session:
        yield session