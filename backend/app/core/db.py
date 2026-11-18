from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.core.config import settings


#Синхронный движок
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Пока True для отладки - показывает SQL-запросы в консоли
)

# Фабрика сессий
SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей SQLAlchemy."""
    pass


def get_db():
    """Зависимость FastAPI для получения сессии БД."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()