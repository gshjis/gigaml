from sqlalchemy.ext.asyncio import AsyncSession
from app.repository.user_repository import UserRepository
from app.schemas.user import UserCreate, UserOut
from app.core.auth import get_password_hash, create_access_token, decode_token
from app.core.exceptions import UserAlreadyExistsError

class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def register_user(self, user: UserCreate) -> UserOut:
        existing_user = await self.repository.get_user_by_email(user.email)
        if existing_user:
            raise UserAlreadyExistsError("User with this email already exists")

        user_copy: UserCreate = user.copy()
        user_copy.password = get_password_hash(user.password)
        db_user = await self.repository.create_user(user_copy)
        return UserOut.from_orm(db_user)

    async def refresh_token(self, refresh_token: str) -> dict:
        payload = decode_token(refresh_token)
        if not payload:
            raise ValueError("Invalid refresh token")

        user = await self.repository.get_user_by_email(payload["sub"])
        if not user:
            raise ValueError("User not found")

        new_access_token = create_access_token(data={"sub": user.email})
        return {"access_token": new_access_token, "token_type": "bearer"}
