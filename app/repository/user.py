from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.core.exceptions import UserAlreadyExistsException, UserNotFoundException
from app.domain import UserData
from app.models.user import User


class UserRepository:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_user_by_email(self, email: str) -> Optional[UserData]:
        """Получить пользователя по email.

        Args:
            email (str): Email пользователя

        Returns:
            Optional[UserData]: Пользователь или None, если пользователь не найден

        Raises:
            UserNotFoundException: Если пользователь не найден
        """
        result = await self.db_session.execute(
            select(User).filter(User.email == email).options(selectinload(User.tasks))
        )
        user = result.scalar_one_or_none()
        print("__" * 30)
        if user:
            return UserData(
                user_id=user.ID,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
            )
        raise UserNotFoundException

    async def create_user(self, user: UserData) -> UserData:
        """Создать нового пользователя.

        Args:
            user (UserData): Данные пользователя

        Returns:
            UserData: Созданный пользователь

        Raises:
            UserAlreadyExistsException: Если пользователь с таким email уже существует
        """
        # Проверка наличия пользователя с таким же адресом электронной почты
        existing_user = await self.get_user_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsException

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=user.hashed_password,
        )
        self.db_session.add(db_user)
        await self.db_session.commit()
        await self.db_session.refresh(db_user)
        return UserData(
            user_id=db_user.ID,
            username=db_user.username,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
        )

    async def get_user_by_username(self, username: str) -> Optional[UserData]:
        """Получить пользователя по имени.

        Args:
            username (str): Имя пользователя

        Returns:
            Optional[UserData]: Пользователь или None, если пользователь не найден

        Raises:
            UserNotFoundException: Если пользователь не найден
        """
        result = await self.db_session.execute(
            select(User).filter(User.username == username)
        )
        user = result.scalar_one_or_none()
        if user:
            return UserData(
                user_id=user.ID,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
            )
        raise UserNotFoundException

    async def get_user_by_id(self, user_id: int) -> Optional[UserData]:
        """Получить пользователя по ID.

        Args:
            user_id (int): ID пользователя

        Returns:
            Optional[UserData]: Пользователь или None, если пользователь не найден

        Raises:
            UserNotFoundException: Если пользователь не найден
        """
        result = await self.db_session.execute(select(User).filter(User.ID == user_id))
        user = result.scalar_one_or_none()
        if user:
            return UserData(
                user_id=user.ID,
                username=user.username,
                email=user.email,
                hashed_password=user.hashed_password,
            )
        raise UserNotFoundException(f"User with ID {user_id} not found")
