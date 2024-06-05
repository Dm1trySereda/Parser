# from sqlalchemy import String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models.base import Base
#
#
# class BaseRole(Base):
#     __tablename__ = "roles"
#
#     id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
#     title: Mapped[str] = mapped_column(String(255))
#     description: Mapped[str] = mapped_column(String(255), nullable=True)
#
#     users_relationship = relationship("BaseUser", back_populates="role_relationship")
