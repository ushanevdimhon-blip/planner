from app.core.db import engine, Base
from app.modules.users.models import User, Role, Organization


def test_connection():
    """Проверяем подключение к БД и создаём таблицы."""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Подключение успешно! Таблицы созданы.")
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
    finally:
        engine.dispose()


if __name__ == "__main__":
    test_connection()