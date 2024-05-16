from sqlalchemy import DECIMAL, BigInteger, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_models import Base


class BooksHistory(Base):
    __tablename__ = "books_history"

    book_id: Mapped[int] = mapped_column(ForeignKey("books.id"))
    book = relationship("Book", back_populates="books_history")
    book_num: Mapped[int] = mapped_column(BigInteger, unique=False, nullable=True)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
