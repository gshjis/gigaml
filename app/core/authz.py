from fastapi import Depends, HTTPException, status, Request, Response
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from typing import Callable, Dict, Optional

from app.core.auth import decode_token
from app.core.permissions import Role, Permission
from app.models.user import User
from app.core.database import get_db_session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_current_user(
    request: Request, 
    response: Response,
    db: AsyncSession = Depends(get_db_session)
    ) -> Dict:
    return {}
    


def require_role(role: Role) -> Callable:
    async def dependency(user: User = Depends(get_current_user)) -> User:
        if user.role != role:
            logger.error(f"User {user.email} does not have the required role: {role}. User Role: {user.role}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return dependency

def require_permission(permission: Permission) -> Callable:
    async def dependency(user: User = Depends(get_current_user)) -> Optional[User]:
        logger.error(f"Permission: {permission}, User Permissions: {user.permissions}")
        if permission.value not in user.permissions:
            logger.error(f"User {user.email} does not have the required permission: {permission}. User Permissions: {user.permissions}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return dependency
