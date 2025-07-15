# app/models/task.py
import logging

logger = logging.getLogger(__name__)

from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

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
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    owner: Mapped["User"] = relationship("User", back_populates="tasks")
