from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class AuthProvider(Base):
    __tablename__ = "auth_provider_users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    provider: Mapped[str] = mapped_column(String(255), nullable=False)
    remote_user_id: Mapped[str] = mapped_column(
        String(length=255), nullable=True, unique=True
    )
    full_name: Mapped[str] = mapped_column(String(255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    user_relationship = relationship(
        "User",
        back_populates="external_user_relationship",
        cascade="all, delete-orphan",
        single_parent=True,
    )


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(length=255))
    title: Mapped[str] = mapped_column(String(length=255))
    description: Mapped[str] = mapped_column(String(length=255), nullable=True)

    users_relationship = relationship("User", back_populates="role_relationship")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(
        String(length=255), nullable=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=True, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=3)
    confirmation_code: Mapped[int] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )

    role_relationship = relationship("Role", back_populates="users_relationship")
    external_user_relationship = relationship(
        "AuthProvider", back_populates="user_relationship", uselist=False
    )
