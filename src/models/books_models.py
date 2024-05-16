from sqlalchemy import DECIMAL, BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_models import Base


class Book(Base):
    __tablename__ = "books"

    book_num: Mapped[int] = mapped_column(BigInteger)
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    price_new: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    price_old: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    discount: Mapped[str] = mapped_column(String(20), nullable=True)
    rating: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=True)
    image: Mapped[str] = mapped_column(String(255))
    book_history = relationship("BookHistory", back_populates="book")
