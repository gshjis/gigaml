from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import create_access_token, create_refresh_token, verify_password, decode_token
from app.core.database import get_db_session
from app.schemas.user import UserCreate, UserOut
from app.service.user_service import UserService
from app.core.dependencies import get_user_service
from app.core.exceptions import UserAlreadyExistsError

router = APIRouter()


@router.post("/register", response_model=UserOut)
async def register_user(
    user: UserCreate,
    service: UserService = Depends(get_user_service)
    ):

    try:
        return await service.register_user(user)
        
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login", response_model=dict)
async def login_user(form_data: OAuth2PasswordRequestForm = Depends(), 
                     service: UserService = Depends(get_user_service)):
    user = await service.repository.get_user_by_email(form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=dict)
async def refresh_token(refresh_token: str):
    async with get_db_session() as db:
        service = UserService(db)
        return await service.refresh_token(refresh_token)
