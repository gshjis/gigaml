# app/schemas/task.py
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator, model_validator


class TaskBaseSchema(BaseModel):
    """Базовая схема с общими полями и валидацией"""

    name: str = Field(
        default="Unnamed Task",
        max_length=80,
        description="Название задачи",
        examples=["Моя задача"],
    )
    pomodoro_count: int = Field(
        default=1, gt=0, description="Количество помодоро", examples=[4]
    )
    category_id: int = Field(gt=0, description="ID категории", examples=[1])
    description: Optional[str] = Field(
        default=None,
        max_length=200,
        description="Описание задачи",
        examples=["Нужно сделать это и то"],
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()


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

    class Config:
        from_attributes = True


class TaskSchemaUpdate(BaseModel):
    """Схема для обновления задачи"""

    name: Optional[str] = Field(
        None, max_length=80, description="Новое название задачи"
    )
    pomodoro_count: Optional[int] = Field(
        None, gt=0, description="Новое количество помодоро"
    )
    category_id: Optional[int] = Field(None, gt=0, description="Новая категория")
    description: Optional[str] = Field(
        None, max_length=200, description="Новое описание"
    )

    @model_validator(mode="before")
    @classmethod
    def validate_update_data(cls, data: Any) -> Any:
        if not data or all(v is None for v in data.values()):
            raise ValueError("Должно быть указано хотя бы одно поле для обновления")
        return data

    @field_validator("name")
    @classmethod
    def validate_updated_name(cls, v: Optional[str]) -> Optional[str]:
        return v.strip() if v else None
