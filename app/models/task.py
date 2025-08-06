from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base, SoftDeleteMixin

if TYPE_CHECKING:
    from app.models.user import User


class Task(Base, SoftDeleteMixin):
    """
    Модель задачи с поддержкой мягкого удаления.
    Наследует:
    - id, created_at, updated_at из Base
    - is_deleted из SoftDeleteMixin
    """

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    pomodoro_count: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
    category_id: Mapped[int] = mapped_column(Integer, nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="tasks")
