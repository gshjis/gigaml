# app/models/task.py
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, SoftDeleteMixin


class Task(Base, SoftDeleteMixin):
    """
    Модель задачи с поддержкой мягкого удаления.
    Наследует:
    - id, created_at, updated_at из Base
    - is_deleted из SoftDeleteMixin
    """

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    pomodoro_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str] = mapped_column(String(100), nullable=True)
