from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base

class Categorie(Base):

    name:Mapped[str] = mapped_column(String(50), nullable=False)
    description:Mapped[str] = mapped_column(String(100), nullable=True)