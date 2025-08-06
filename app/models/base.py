from datetime import datetime

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column


class SoftDeleteMixin:
    """Mixin for soft delete"""

    is_deleted: Mapped[bool] = mapped_column(default=False)


class Base(AsyncAttrs, DeclarativeBase, SoftDeleteMixin):
    """Base model"""

    __abstract__ = True

    ID: Mapped[int] = mapped_column("id", primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower() + "s"
