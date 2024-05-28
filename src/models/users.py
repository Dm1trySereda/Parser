from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(length=255), nullable=True, unique=True
    )
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=False, index=True, nullable=False
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
