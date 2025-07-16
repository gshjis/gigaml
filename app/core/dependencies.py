from app.service.user import UserService
from app.core.database import get_db_session

from typing import Annotated, Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository import BaseRepository, TaskRepository, UserRepository
from app.service import TaskService, UserService

T = Type

async def get_user_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    return UserService(UserRepository(db_session))

async def get_task_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TaskService:
    """Фабрика зависимостей для сервиса задач"""
    return TaskService(TaskRepository(db_session))
