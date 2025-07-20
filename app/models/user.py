from sqlalchemy import String, Boolean, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING

from app.models.base import Base
import json

from app.core.permissions import Role, Permission, RoleEnum

if TYPE_CHECKING:
    from app.models.task import Task
    
class User(Base):
    
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_superuser: Mapped[bool] = mapped_column(Boolean, default=False)
    role: Mapped[Role] = mapped_column(RoleEnum, default=Role.USER)
    permissions: Mapped[List[str]] = mapped_column(ARRAY(Text), default=json.dumps(Permission.ALL))
    refresh_token: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    tasks: Mapped[List[Task]] = relationship("Task", back_populates="owner")