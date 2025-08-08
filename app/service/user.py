from datetime import timedelta
from typing import Any, Dict, Optional

from app.core.exceptions import InvalidCredentialsException, InvalidTokenException
from app.core.settings import settings
from app.domain import UserData
from app.repository.user import UserRepository
from app.security.auth import create_jwt, from_token, get_password_hash, verify_password


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(
        self, username: str, email: str, password: str
    ) -> Dict[str, str | UserData]:
        """Регистрация нового пользователя

        Args:
            username (str): Имя пользователя
            email (str): Email пользователя
            password (str): Пароль пользователя

        Returns:
            Dict[str, str | UserData]: Данные пользователя, access token и refresh token
        """
        hashed_password = get_password_hash(password)
        user_data = UserData(
            user_id=1,  # заглушка, ведь до создания у нас нет ID (ID генерируется сам)
            username=username,
            email=email,
            hashed_password=hashed_password,
        )
        user = await self.repository.create_user(user_data)

        # Generate JWT token
        token_data = {
            "sub": str(user.user_id),
            "username": user.username,
            "email": user.email,
        }

        access_token_expires = timedelta(
            minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token_expires = timedelta(
            minutes=float(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        )
        access_token = create_jwt(
            data=token_data,
            algorithm=settings.ALGORITHM,
            secret_key=settings.SECRET_KEY,
            exp_timedelta=access_token_expires,
        )
        refresh_token = create_jwt(
            data=token_data,
            algorithm=settings.ALGORITHM,
            secret_key=settings.SECRET_KEY,
            exp_timedelta=refresh_token_expires,
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def authentication(
        self, email_or_username: str, password: str
    ) -> Dict[str, Any]:
        """Аутентификация пользователя

        Args:
            email_or_username (str): Email или имя пользователя
            password (str): Пароль пользователя

        Returns:
            Dict[str, Any]: Данные пользователя, access token и refresh token

        Raises:
            InvalidCredentialsException: Если пользователь не найден или пароль неверный
        """
        # Retrieve the user by email or username

        if "@" in email_or_username:
            user = await self.repository.get_user_by_email(email_or_username)
        else:
            user = await self.repository.get_user_by_username(email_or_username)

        if user is None or not verify_password(password, user.hashed_password):
            raise InvalidCredentialsException

        # Generate JWT token
        token_data = {
            "sub": str(user.user_id),
            "username": user.username,
            "email": user.email,
        }

        access_token_expires = timedelta(
            minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        # Генерация refresh токена
        refresh_token_expires = timedelta(
            minutes=float(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        )
        refresh_token = create_jwt(
            data=token_data,
            algorithm=settings.ALGORITHM,
            secret_key=settings.SECRET_KEY,
            exp_timedelta=refresh_token_expires,
        )
        access_token = create_jwt(
            data=token_data,
            algorithm=settings.ALGORITHM,
            secret_key=settings.SECRET_KEY,
            exp_timedelta=access_token_expires,
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    async def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Получить пользователя по ID.

        Args:
            user_id (int): ID пользователя

        Returns:
            Dict[str, Any]: Пользователь или None, если пользователь не найден
        """
        user = await self.repository.get_user_by_id(user_id)
        if user:
            return {
                "user_id": user.user_id,
                "username": user.username,
                "email": user.email,
                "hashed_password": user.hashed_password,
            }
        return {}

    async def refresh(self, refresh_token: Optional[str]) -> Dict[str, str]:
        """Обновление токенов

        Args:
            refresh_token (Optional[str]): Refresh токен

        Returns:
            Dict[str, str]: Новые access и refresh токены

        Raises:
            InvalidTokenException: Если refresh токен не передан
            InvalidCredentialsException: Если refresh токен недействителен или пользователь не найден
        """
        try:
            if refresh_token is None:
                raise InvalidTokenException
            payload = from_token(
                refresh_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM
            )
            user_id = payload.get("sub")
            username = payload.get("username")
            email = payload.get("email")

            if not user_id or not username or not email:
                raise InvalidCredentialsException("Invalid refresh token")

            # Получение пользователя из базы данных
            user = await self.repository.get_user_by_id(int(user_id))

            if not user:
                raise InvalidCredentialsException("User not found")

            # Генерация нового access токена
            access_token_expires = timedelta(
                minutes=float(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            access_token = create_jwt(
                data={
                    "sub": str(user.user_id),
                    "username": user.username,
                    "email": user.email,
                },
                algorithm=settings.ALGORITHM,
                secret_key=settings.SECRET_KEY,
                exp_timedelta=access_token_expires,
            )

            # Генерация нового refresh токена
            refresh_token_expires = timedelta(
                minutes=float(settings.REFRESH_TOKEN_EXPIRE_MINUTES)
            )
            new_refresh_token = create_jwt(
                data={
                    "sub": str(user.user_id),
                    "username": user.username,
                    "email": user.email,
                },
                algorithm=settings.ALGORITHM,
                secret_key=settings.SECRET_KEY,
                exp_timedelta=refresh_token_expires,
            )

            return {"access_token": access_token, "refresh_token": new_refresh_token}

        except Exception as e:
            raise InvalidCredentialsException(str(e))
