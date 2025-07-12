from typing import Annotated, Callable, Type

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.repository import BaseRepository, TaskRepository
from app.service.task import TaskService

T = Type

async def get_repository(repo_type: Type[T]) -> Callable[[AsyncSession], T]:
    """Фабрика зависимостей для репозиториев"""

    async def _get_repo(
        db_session: Annotated[AsyncSession, Depends(get_db_session)]
    ) -> T:
        return repo_type(db_session)

    return _get_repo

async def get_task_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TaskService:
    """Фабрика зависимостей для сервиса задач"""
    return TaskService(TaskRepository(db_session))
