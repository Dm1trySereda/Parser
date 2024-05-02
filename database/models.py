from datetime import datetime

from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import String, Date, DECIMAL, ForeignKey, Column, Integer, BigInteger


class Base(DeclarativeBase):
    pass


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[datetime] = mapped_column(default=datetime.now().date())
    book_num: Mapped[int] = mapped_column(nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=True)
    author: Mapped[str] = mapped_column(String(255), nullable=True)
    price_new: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    price_old: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=True)
    discount: Mapped[str] = mapped_column(String(20), nullable=True)
    rating: Mapped[float] = mapped_column(DECIMAL(4, 2), nullable=True)
    image: Mapped[str] = mapped_column(String(255))
    books_history = relationship("BooksHistory", back_populates="books")


class BooksHistory(Base):
    __tablename__ = "books_history"

    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'), primary_key=True)
    books = relationship("Book", back_populates="books_history")
    date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    book_num: Mapped[int] = mapped_column(unique=False)
    title: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
