import os
from dotenv import load_dotenv
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Загрузка .env
load_dotenv()
db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise ValueError("DATABASE_URL не найден в .env")

# Конфигурация Alembic
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Метаданные ваших моделей
from app.models import Base
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Миграции в offline-режиме (без подключения к БД)."""
    context.configure(
        url=db_url,  # Используем URL из .env
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Миграции в online-режиме (с подключением к БД)."""
    # Переопределяем конфиг, подставляя наш URL
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = db_url  # Важно!

    connectable = engine_from_config(
        configuration,  # Используем модифицированный конфиг
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()