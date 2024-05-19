from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String


class Role(Base):
    __tablename__ = "roles"

    role: Mapped[str] = mapped_column(String(255), nullable=False)
    user = relationship("User", back_populates="role")
