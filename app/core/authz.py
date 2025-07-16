from fastapi import Depends, HTTPException, status, Request, Response
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
import logging

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
    ):
    
    logger.info("Retrieving current user")
    access_token = request.cookies.get("access_token")

    if not access_token:
        logger.error("Missing access token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    payload = decode_token(access_token)
    if not payload:
        # If access token is invalid or expired, check for refresh token
        refresh_token = request.cookies.get("refresh_token")
        if refresh_token:
            payload = decode_token(refresh_token)
            if payload:
                # Generate a new access token
                new_access_token = create_access_token({"sub": payload["sub"]})
                # Set the new access token in the response cookies
                response.set_cookie(key="access_token", value=new_access_token, httponly=True)
                return response, payload
    if not payload:
        logger.error("Invalid token")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

    user = await db.get(User, int(payload["sub"]))
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")

    logger.info(f"User retrieved: {user.email}")
    return user

def require_role(role: Role):
    async def dependency(user: User = Depends(get_current_user)):
        if user.role != role:
            logger.error(f"User {user.email} does not have the required role: {role}. User Role: {user.role}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return dependency

def require_permission(permission: Permission):
    async def dependency(user: User = Depends(get_current_user)):
        logger.error(f"Permission: {permission}, User Permissions: {user.permissions}")
        if permission.value not in user.permissions:
            logger.error(f"User {user.email} does not have the required permission: {permission}. User Permissions: {user.permissions}")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return user
    return dependency
