from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.core.settings import settings
from app.models.user import User
from app.repository import TaskRepository, UserRepository
from app.security.auth import from_token, oauth2_scheme
from app.service import TaskService, UserService


async def get_user_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> UserService:
    return UserService(UserRepository(db_session))


async def get_task_service(
    db_session: Annotated[AsyncSession, Depends(get_db_session)],
) -> TaskService:
    """Фабрика зависимостей для сервиса задач"""
    return TaskService(TaskRepository(db_session))


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    service: Annotated[UserService, Depends(get_user_service)],
) -> User:
    token_data = from_token(
        token=token, secret_key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
    )
    user_id = int(token_data["sub"])
    user_data = await service.get_user_by_id(user_id=user_id)

    # Преобразование user_data в объект User
    user = User(
        ID=user_data["user_id"],
        username=user_data["username"],
        email=user_data["email"],
        hashed_password=user_data["hashed_password"],
    )

    return user
