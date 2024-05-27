# from sqlalchemy import String
# from sqlalchemy.orm import Mapped, mapped_column, relationship
#
# from src.models.base import Base
#
#
# class Role(Base):
#     __tablename__ = "roles"
#
#     role: Mapped[str] = mapped_column(String(255), nullable=False)
#     user = relationship("User", back_populates="role")
# #