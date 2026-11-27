import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импорт настроек из .env и базового класса
from app.core.config import settings
from app.core.db import Base

# Импорт ВСЕХ моделей, чтобы Alembic их увидел в Base.metadata
# Если забудешь импорт — autogenerate решит, что таблиц нет,
#    и сгенерирует DROP TABLE для всего.
from app.modules.users.models import User, Role, Organization
from app.modules.projects.models import Project
from app.modules.teams.models import Team, TeamMember
from app.modules.tasks.models import Epic, Task, Subtask
from app.modules.invitations.models import Invitation

# Alembic Config object
config = context.config

# Переопределяем URL из .env (пароль не светится в alembic.ini)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Настройка логирования (если в ini есть секция [loggers])
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные для autogenerate
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Offline-режим: генерирует SQL-скрипт без подключения к БД."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Синхронная часть: выполняется внутри async-соединения через run_sync."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Асинхронный запуск миграций (наш основной путь)."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Online-режим: применяет миграции к реальной БД."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()