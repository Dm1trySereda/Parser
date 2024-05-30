from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base



class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=func.now(), onupdate=func.now()
    )
    username: Mapped[str] = mapped_column(
        String(length=255), nullable=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=False)
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=False, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # user_role = relationship("UserRole", back_populates="user", uselist=False)
