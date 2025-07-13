# Pomodoro FastAPI

Pomodoro FastAPI is a time management tool designed to help you work with the Pomodoro Technique. The application is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.

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
uvicorn app.core.main:app --reload
```

## Running Docker Compose

To run the application using Docker Compose, use the following command:

```bash
docker-compose up --build
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

## Development

To run the development server with auto-reloading, use:

```bash
poetry run uvicorn app.core.main:app --reload
```

## Linters and Formatters

The project uses the following linters and formatters:

- Flake8
- Pylint
- MyPy
- Black
- Isort
- Bandit

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

class CategorySchema(BaseModel):
    id: int
    name: str
```

### TaskSchema

```python
from datetime import datetime
from typing import Any, Optional, Annotated
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict, StringConstraints

# Общие ограничения для повторного использования
NameStr = Annotated[str, StringConstraints(strip_whitespace=True, max_length=80)]
DescriptionStr = Annotated[Optional[str], StringConstraints(max_length=200)]

class TaskBaseSchema(BaseModel):
    """Базовая схема с общими полями и валидацией"""
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        },
        from_attributes=True,
        str_strip_whitespace=True
    )

    name: NameStr = Field(
        default="Unnamed Task",
        description="Название задачи",
        examples=["Моя задача"],
    )

    pomodoro_count: int = Field(
        default=1,
        gt=0,
        description="Количество помодоро",
        examples=[4]
    )

    category_id: int = Field(
        gt=0,
        description="ID категории",
        examples=[1]
    )

    description: DescriptionStr = Field(
        default=None,
        description="Описание задачи",
        examples=["Нужно сделать это и то"],
    )

class TaskSchemaInput(TaskBaseSchema):
    """Схема для создания задачи"""
    @model_validator(mode="before")
    @classmethod
    def generate_default_name(cls, data: Any) -> Any:
        if isinstance(data, dict) and not data.get("name"):
            data["name"] = f"Task {data.get('id', 'new')}"
        return data

class TaskSchemaOutput(TaskBaseSchema):
    """Схема для вывода задачи"""
    id: int = Field(..., gt=0, description="ID задачи")
    created_at: datetime
    updated_at: datetime
    is_deleted: bool = Field(
        False,
        description="Флаг удаления",
        exclude=True  # Исключаем из вывода, если не удалено
    )

class TaskSchemaUpdate(TaskBaseSchema):
    """Схема для обновления задачи"""
    model_config = ConfigDict(
        json_encoders={
            datetime: lambda v: v.isoformat()
        }
    )

    name: Optional[NameStr] = Field(
        None,
        description="Новое название задачи"
    )

    pomodoro_count: Optional[int] = Field(
        None,
        gt=0,
        description="Новое количество помодоро"
    )

    category_id: Optional[int] = Field(
        None,
        gt=0,
        description="Новая категория"
    )

    description: DescriptionStr = Field(
        None,
        description="Новое описание"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_update_data(cls, data: Any) -> Any:
        if not data or all(v is None for v in data.values()):
            raise ValueError("Должно быть указано хотя бы одно поле для обновления")
        return data
```

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## License

This project is licensed under the MIT License.
