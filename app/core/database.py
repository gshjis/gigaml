# app/core/database.py
from typing import AsyncIterator
import logging
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from app.core.logging_config import logger
from app.core.settings import settings

DATABASE_URL = settings.DATABASE_URL

engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=True,
    pool_pre_ping=True,
)
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


async def get_db_session() -> AsyncIterator[AsyncSession]:
    """Return async DB session"""
    async with AsyncSessionLocal() as session:
        try:
            logger.info("Session opened")
            yield session
        finally:
            await session.close()
            logger.info("Session closed")
