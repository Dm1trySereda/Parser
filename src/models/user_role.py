# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models.base import Base
#
#
# class UserRole(Base):
#     __tablename__ = "user_roles"
#
#     user_id: Mapped[int] = mapped_column(
#         ForeignKey("users.id"), primary_key=True, nullable=True
#     )
#     role_id: Mapped[int] = mapped_column(
#         ForeignKey("roles.id"), primary_key=True, nullable=True
#     )
#     role = relationship("Role", back_populates="user_role")
#     user = relationship("User", back_populates="user_role", uselist=False)
