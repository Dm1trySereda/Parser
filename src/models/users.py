from datetime import datetime

from sqlalchemy import TIMESTAMP, Boolean, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class BaseRole(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255))
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users_relationship = relationship("BaseUser", back_populates="role_relationship")

    # permissions = relationship(
    #     "Permission", secondary="role_permissions", back_populates="roles"
    # )


class BaseUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow
    )
    username: Mapped[str] = mapped_column(
        String(length=255), nullable=True, unique=True
    )
    hashed_password: Mapped[str] = mapped_column(String(length=1024), nullable=True)
    full_name: Mapped[str] = mapped_column(String(length=255), nullable=True)
    email: Mapped[str] = mapped_column(
        String(length=320), unique=False, index=True, nullable=False
    )
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_google_user: Mapped[bool] = mapped_column(Boolean, default=False)
    role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), default=3)

    role_relationship = relationship("BaseRole", back_populates="users_relationship")


# class Permission(Base):
#     __tablename__ = "permissions"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     name: Mapped[str] = mapped_column(String(length=255), nullable=False, unique=True)
#     description: Mapped[str] = mapped_column(String(length=255), nullable=True)
#
#     roles = relationship(
#         "BaseRole", secondary="role_permissions", back_populates="permissions"
#     )
#
#
# class RolePermission(Base):
#     __tablename__ = "role_permissions"
#
#     role_id: Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
#     permission_id: Mapped[int] = mapped_column(
#         ForeignKey("permissions.id"), primary_key=True
#     )
#     role = relationship("BaseRole")
#     permission = relationship("Permission")
