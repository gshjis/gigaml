from fastapi import APIRouter, Depends, HTTPException, status, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

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
    ):

    try:
        return await service.register_user(user)
        
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/login", response_model=dict)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(), 
    service: UserService = Depends(get_user_service)
    ):
    user = await service.repository.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.id})
    refresh_token = create_refresh_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="lax")

    return {"detail": "Logged in successfully"}


@router.post("/refresh", response_model=dict)
async def refresh_token(
    refresh_token: str,
    response: Response,
    service: UserService = Depends(get_user_service)
    ):
    user = await service.repository.get_user_by_refresh_token(refresh_token)
    access_token = create_access_token(data={"sub": user.id})
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="lax")
    return {"detail": "Token refreshed successfully"}
