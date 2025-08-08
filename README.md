# Pomodoro FastAPI

Pomodoro FastAPI is a time management tool designed to help you work with the Pomodoro Technique. The application is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.12+ based on standard Python type hints.

## Features

- Task management with the Pomodoro Technique.
- User authentication and authorization.
- Real-time updates and notifications.
- Caching for improved performance.

## Installation

To install the project dependencies, run:

```bash
poetry install
```

## Configuration

Create a `.env` file in the project root with the following content:

```env
DATABASE_URL=postgresql://user:password@localhost/dbname
REDIS_URL=redis://localhost:6379/0
```

## Running the Application

To run the application, use the following command:

```bash
make run_container
```

## Opening the Backend and Frontend

- The backend will be available at `http://localhost:8000`.
- The frontend will be available at `http://localhost:8080`.

## Dependencies

The project dependencies are specified in the `pyproject.toml` file. The main dependencies include:

- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- Alembic
- Psycopg2-binary
- Redis
- Python-dotenv

## Linters and Formatters

The project uses the following linters and formatters:

- Flake8
- MyPy
- Black
- Isort

## Testing

To run the tests, use:

```bash
poetry run pytest
```

## API Documentation

The API documentation is available at `http://localhost:8000/docs`.

## Schemas

### CategorySchema

```python
from pydantic import BaseModel

class CategorySchemaInput(BaseModel):
    name: str

class CategorySchemaOutput(BaseModel):
    category_id: int
    name: str
```

### TaskSchema

```python
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TaskSchemaInput(BaseModel):
    name: str
    description: Optional[str] = None
    pomodoro_count: int
    category_id: int

    class Config:
        from_attributes = True

class TaskSchemaUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    pomodoro_count: Optional[int] = None
    category_id: Optional[int] = None

    class Config:
        from_attributes = True

class TaskSchemaOutput(BaseModel):
    task_id: int
    name: str
    description: Optional[str] = None
    pomodoro_count: int
    category_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### UserSchema

```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    user_id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True
```

## Database Models

### Category

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base

class Categorie(Base):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
```

### Task

```python
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User

class Task(Base, SoftDeleteMixin):
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    pomodoro_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tasks")
```

### User

```python
from typing import TYPE_CHECKING, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if TYPE_CHECKING:
    from app.models.task import Task

class User(Base):
    username: Mapped[str] = mapped_column(
        String, unique=True, index=True, nullable=False
    )
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)

    tasks: Mapped[Optional[list["Task"]]] = relationship("Task", back_populates="owner")
```

## Possible Errors

### UserAlreadyExistsException

```python
class UserAlreadyExistsException(HTTPException):
    def __init__(self, message: str = "User with this email already exists"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=message,
        )
```

### UserNotFoundException

```python
class UserNotFoundException(HTTPException):
    def __init__(self, message: str = "User not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
```

### InvalidCredentialsException

```python
class InvalidCredentialsException(HTTPException):
    def __init__(self, message: str = "Invalid credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
```

### InvalidTokenException

```python
class InvalidTokenException(HTTPException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=message,
        )
```

### TaskNotFoundException

```python
class TaskNotFoundException(HTTPException):
    def __init__(self, message: str = "Task not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=message,
        )
```

### DatabaseError

```python
class DatabaseError(HTTPException):
    def __init__(self, message: str = "Database error"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=message,
        )
```

## Handlers

### Authentication Handlers

#### Register User

```python
@router.post(
    "/register",
    response_model=dict,
    summary="Регистрация нового пользователя",
    description="""Этот маршрут позволяет зарегистрировать нового пользователя в системе.
    В случае успешной регистрации возвращается информация о пользователе и токены доступа.""",
    status_code=status.HTTP_201_CREATED,
)
async def register_user(
    user: UserCreate,
    response: Response,
    service: UserService = Depends(get_user_service),
) -> Dict[str, Any]:
    payload = await service.register_user(
        username=user.username, email=user.email, password=user.password
    )
    new_user = payload.get("user", None)
    access_token = payload["access_token"]
    refresh_token = str(payload["refresh_token"])

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME, value=refresh_token, httponly=True
    )

    return {
        "user": new_user,
        "access_token": access_token,
        "token_type": "bearer",
    }
```

#### Login User

```python
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
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
) -> Dict[str, Any]:
    payload = await service.authentication(
        email_or_username=form_data.username, password=form_data.password
    )

    access_token = payload["access_token"]
    refresh_token = str(payload["refresh_token"])

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME, value=refresh_token, httponly=True
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
```

#### Refresh Token

```python
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
    service: UserService = Depends(get_user_service),
) -> Dict[str, Any]:
    refresh_token = request.cookies.get(str(settings.REFRESH_TOKEN_COOKIES_NAME))
    tokens = await service.refresh(refresh_token)
    new_refresh_token = tokens["refresh_token"]
    access_token = tokens["access_token"]

    response.set_cookie(
        key=settings.REFRESH_TOKEN_COOKIES_NAME,
        value=new_refresh_token,
        httponly=True,
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
```

### Task Handlers

#### Get All Tasks

```python
@router.get(
    "",
    response_model=list[TaskSchemaOutput],
    summary="Get all tasks",
    description="""Этот маршрут позволяет получить все активные задачи.
    В случае успешного получения возвращается список задач.""",
    status_code=status.HTTP_200_OK,
)
async def get_all_tasks(
    user: Annotated[User, Depends(get_current_user)],
    service: Annotated[TaskService, Depends(get_task_service)],
) -> list[TaskSchemaOutput]:
    tasks = await service.get_tasks_by_user_id(user_id=user.ID)
    return [TaskSchemaOutput(**task) for task in tasks]
```

#### Create Task

```python
@router.post(
    "",
    response_model=TaskSchemaOutput,
    summary="Создание новой задачи",
    description="""Этот маршрут позволяет создать новую задачу.
    В случае успешного создания возвращается информация о созданной задаче.""",
    status_code=status.HTTP_201_CREATED,
)
async def create_task(
    task_data: TaskSchemaInput,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> TaskSchemaOutput:
    created_task = await service.create_task(
        name=task_data.name,
        description=task_data.description,
        pomodoro_count=task_data.pomodoro_count,
        category_id=task_data.category_id,
        owner_id=user.ID,
    )
    return TaskSchemaOutput(**created_task)
```

#### Delete Task

```python
@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удаление задачи",
    description="""Этот маршрут позволяет удалить задачу по ID.
    В случае успешного удаления возвращается пустой ответ с кодом 204.""",
)
async def delete_task(
    task_id: int,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> Response:
    await service.delete_task(task_id, user_id=user.ID)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
```

#### Update Task

```python
@router.patch(
    "/{task_id}",
    response_model=TaskSchemaOutput,
    summary="Обновление задачи",
    description="""Этот маршрут позволяет частично обновить задачу.
    В случае успешного обновления возвращается обновленная информация о задаче.""",
    status_code=status.HTTP_200_OK,
)
async def update_task(
    task_id: int,
    update_data: TaskSchemaUpdate,
    service: Annotated[TaskService, Depends(get_task_service)],
    user: Annotated[User, Depends(get_current_user)],
) -> TaskSchemaOutput:
    updated_task = await service.update_task(
        task_id=task_id,
        owner_id=user.ID,
        name=update_data.name,
        description=update_data.description,
        pomodoro_count=update_data.pomodoro_count,
        category_id=update_data.category_id,
    )
    return TaskSchemaOutput(**updated_task)
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
