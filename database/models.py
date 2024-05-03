from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Date, DECIMAL, ForeignKey, Column, Integer, BigInteger


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(book_num={self.book_num}, title={self.title}, author={self.author}, price_new={self.price_new}, price_old={self.price_old}, discount={self.discount}, rating={self.rating}, image={self.image})"


class Book(Base):
    __tablename__ = "books"

    date: Mapped[datetime] = mapped_column(default=datetime.now().date())
    book_num: Mapped[int]
    title: Mapped[str] = mapped_column(String(255))
    author: Mapped[str] = mapped_column(String(255))
    price_new: Mapped[float] = mapped_column(DECIMAL(10, 2))
    price_old: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    discount: Mapped[str] = mapped_column(String(20), nullable=True)
    rating: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=True)
    image: Mapped[str] = mapped_column(String(255))
    books_history = relationship("BooksHistory", back_populates="book")


class BooksHistory(Base):
    __tablename__ = "books_history"

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    book = relationship("Book", back_populates="books_history")
    date: Mapped[datetime] = mapped_column(default=datetime.now().date())
    book_num: Mapped[int] = mapped_column(unique=False)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
