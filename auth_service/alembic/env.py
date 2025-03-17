import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context
from config import settings
from models import Base


# Загружаем конфигурацию Alembic
config = context.config
config.set_main_option("sqlalchemy.url", settings.async_database_url)

# Логирование
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные моделей
target_metadata = Base.metadata


def run_migrations_offline():
    """Запускает Alembic в оффлайн-режиме (без подключения к БД)."""
    context.configure(
        url=settings.async_database_url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection):
    """Настройка контекста Alembic и выполнение миграций."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations():
    """Запуск Alembic в асинхронном режиме."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online():
    """Запускает Alembic в онлайн-режиме с подключением к БД."""
    asyncio.run(run_async_migrations())


# Определяем режим работы и запускаем миграции
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
