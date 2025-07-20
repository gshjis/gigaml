from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict

from app.core.auth import create_access_token, create_refresh_token, verify_password, decode_token
from app.core.database import get_db_session
from app.schemas.user import UserCreate, UserOut
from app.service.user import UserService
from app.core.dependencies import get_user_service
from app.core.exceptions import UserAlreadyExistsError

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=UserOut)
async def register_user(
    user: UserCreate,
    response: Response,
    service: UserService = Depends(get_user_service)
    ) -> Dict:
    return {}

@router.post("/login", response_model=dict)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service: UserService = Depends(get_user_service)
    ) -> Dict:
    return {}


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    response: Response,
    service: UserService = Depends(get_user_service)
    ) -> Dict:
    return {}
