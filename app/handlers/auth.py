from typing import Any, Dict

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.dependencies import get_user_service
from app.core.settings import settings
from app.schemas.auth import RegisterResponse, TokenResponse
from app.schemas.user import UserCreate, UserOut
from app.service.user import UserService

router = APIRouter(prefix="/auth")


@router.post(
    "/register",
    response_model=RegisterResponse,
    summary="Регистрация нового пользователя",
    description="""Этот маршрут позволяет зарегистрировать нового пользователя в системе.
    В случае успешной регистрации возвращается информация о пользователе и токены доступа.""",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    response: Response,
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> RegisterResponse:
    # Создание нового пользователя в базе данных
    payload = await service.register_user(
        username=user.username, email=user.email, password=user.password
    )
    new_user = payload["user"]
    new_user = UserOut(
        user_id=new_user.user_id, username=new_user.username, email=new_user.email
    )
    access_token = str(payload["access_token"])
    refresh_token = str(payload["refresh_token"])

    # Установка куки для обновления токена
    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME, value=refresh_token, httponly=True
    )

    # Возврат информации о пользователе и токенов
    return RegisterResponse(
        access_token=access_token, token_type="bearer", user=new_user
    )


@router.post(
    "/login",
    response_model=dict,
    summary="Авторизация пользователя",
    description="""Этот маршрут позволяет авторизовать пользователя в системе.
    В случае успешной авторизации возвращается информация о пользователе и токены доступа.""",
    status_code=status.HTTP_200_OK,
)
async def login_user(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),  # noqa: B008
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> Dict[Any, Any]:
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
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    ).model_dump()


@router.post(
    "/refresh",
    response_model=dict,
    summary="Обновление токена",
    description="""Этот маршрут позволяет обновить токен доступа пользователя.
    В случае успешного обновления возвращается новый access токен.""",
    status_code=status.HTTP_200_OK,
)
async def refresh_token(
    response: Response,
    request: Request,
    service: UserService = Depends(get_user_service),  # noqa: B008
) -> TokenResponse:
    refresh_token = request.cookies.get(str(settings.REFRESH_TOKEN_COOKIES_NAME))
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
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )
