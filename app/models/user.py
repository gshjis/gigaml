from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship

from app.models.base import Base
from sqlalchemy import Text
import json

from app.core.permissions import Role, Permission, RoleEnum


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    role = Column(RoleEnum, default=Role.USER)
    permissions = Column(Text, default=json.dumps([Permission.READ.value]))
    
    tasks = relationship("Task", back_populates="owner")
