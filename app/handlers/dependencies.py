from typing import Annotated, Callable, Type, TypeVar

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_session
from app.repository import BaseRepository, TaskRepository
from app.service.task import TaskService

T = TypeVar("T", bound=BaseRepository)


def get_repository(repo_type: Type[T]) -> Callable[[Session], T]:
    """Фабрика зависимостей для репозиториев"""

    def _get_repo(
        db_session: Annotated[Session, Depends(get_db_session)]
    ) -> T:
        return repo_type(db_session)

    return _get_repo


def get_task_service(
    db_session: Annotated[Session, Depends(get_db_session)],
) -> TaskService:
    """Фабрика зависимостей для сервиса задач"""
    return TaskService(TaskRepository(db_session))
