from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_user_service
from app.core.exceptions import InvalidTokenException
from app.core.settings import settings
from app.schemas.user import UserCreate
from app.service.user import UserService

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=dict)
async def register_user(
    user: UserCreate,
    response: Response,
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> Dict[str, Any]:
    # Создание нового пользователя в базе данных
    payload = await service.register_user(
        username=user.username, email=user.email, password=user.password
    )
    new_user = payload.get("user", None)
    access_token = payload["access_token"]
    refresh_token = str(payload["refresh_token"])

    # Установка куки для обновления токена
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME, value=refresh_token, httponly=True
    )

    # Возврат информации о пользователе и токенов
    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login", response_model=dict)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> Dict[str, Any]:
    # Получение пользователя из базы данных
    payload = await service.authentication(
        email_or_username=form_data.username, password=form_data.password
    )

    access_token = payload["access_token"]
    refresh_token = str(payload["refresh_token"])

    # Установка куки для обновления токена
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME, value=refresh_token, httponly=True
    )

    # Возврат информации о пользователе и токенов
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/refresh", response_model=dict)
async def refresh_token(
    response: Response,
    request: Request,
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> Dict[str, Any]:
    refresh_token = request.cookies.get(str(settings.REFRESH_TOKEN_COOKIES_NAME))

    try:
        # Обновление токенов
        tokens = await service.refresh(refresh_token)
        new_refresh_token = tokens["refresh_token"]
        access_token = tokens["access_token"]

        # Установка обновленного refresh токена в куки
        response.set_cookie(
            key=settings.REFRESH_TOKEN_COOKIES_NAME,
            value=new_refresh_token,
            httponly=True,
        )

        # Возврат обновленного access токена
        return {
            "access_token": access_token,
            "token_type": "bearer",
        }

    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )
