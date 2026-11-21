import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

from app.main import app
from app.core.db import get_db, Base
from app.core.security import hash_password
from app.modules.users.models import User
from app.core.config import settings

# Укажите здесь URL ВАШЕЙ ТЕСТОВОЙ базы данных PostgreSQL
# Драйвер обязательно должен быть asyncpg
TEST_DATABASE_URL = settings.TEST_DATABASE_URL

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    poolclass=NullPool
)

# Фабрика сессий для тестов
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Создает все таблицы перед запуском тестов и удаляет после."""
    async with test_engine.begin() as conn:
        # Если база не пустая, можно делать drop_all перед create_all
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_engine.dispose()


@pytest_asyncio.fixture
async def db_session():
    """
    Фикстура изоляции тестов.
    Открывает соединение, запускает транзакцию и делает ROLLBACK после теста.
    """
    connection = await test_engine.connect()
    transaction = await connection.begin()

    # Привязываем сессию к текущему соединению
    session = TestingSessionLocal(bind=connection)

    yield session

    # Откатываем все изменения, сделанные в рамках этого теста
    await session.close()
    await transaction.rollback()
    await connection.close()


@pytest_asyncio.fixture
async def client(db_session):
    """Клиент FastAPI с подмененной зависимостью БД."""

    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def test_user(db_session):
    """Создает тестового пользователя."""
    user = User(
        login="testuser",
        hashed_password=hash_password("testpassword123"),
        email="test@example.com",
        last_name="Иванов",
        first_name="Иван",
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)
    return user