from sqlalchemy import DECIMAL, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import Base


class History(Base):
    __tablename__ = "history"

    book_num: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    book = relationship("Book", back_populates="history")
