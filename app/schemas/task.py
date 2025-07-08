from typing import Any

from pydantic import BaseModel, Field, model_validator


class TaskSchema(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(max_length=80)
    pomodoro_count: int = Field(gt=0)
    category_id: int = Field(gt=0)
    description: str = Field(max_length=200, example = "Task description")

    @model_validator(mode="before")
    @classmethod
    def set_default_name_if_empty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data.get("name") is None:
                data["name"] = f"Task {data.get('id', '?')}"
        return data
