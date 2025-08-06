from datetime import datetime

from pydantic import BaseModel


class TaskSchemaInput(BaseModel):
    name: str
    description: str | None = None
    pomodoro_count: int
    category_id: int

    class Config:
        from_attributes = True


class TaskSchemaUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    pomodoro_count: int | None = None
    category_id: int | None = None

    class Config:
        from_attributes = True


class TaskSchemaOutput(BaseModel):
    task_id: int
    name: str
    description: str | None = None
    pomodoro_count: int
    category_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
