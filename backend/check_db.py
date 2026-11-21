import asyncio
from app.core.db import engine, Base

# Обязательно импортируем модели, чтобы SQLAlchemy знал о них перед create_all
from app.modules.users.models import User, Role, Organization


async def test_connection():
    """Проверяем подключение к БД и создаём таблицы."""
    try:
        # engine.begin() открывает асинхронную транзакцию
        async with engine.begin() as conn:
            # run_sync адаптирует синхронную функцию create_all под асинхронный контекст
            await conn.run_sync(Base.metadata.create_all)

        print("✅ Подключение успешно! Таблицы созданы.")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    finally:
        # Асинхронное закрытие пула соединений
        await engine.dispose()


if __name__ == "__main__":
    # Запускаем асинхронную функцию через asyncio
    asyncio.run(test_connection())