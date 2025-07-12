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