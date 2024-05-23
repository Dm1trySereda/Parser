from typing import Sequence

from sqlalchemy import and_, asc, delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.models import Book
from src.models.books import Book
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def select_book(self, **kwargs) -> Book | Sequence[Book] | None:
        select_values = list()

        if kwargs.get("book_id"):
            select_values.append(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            select_values.append(Book.book_num == kwargs.get("book_num"))
        if kwargs.get("title"):
            select_values.append(Book.title.contains(kwargs.get("title")))
        if kwargs.get("price_new"):
            select_values.append(Book.price_new == kwargs.get("price_new"))
        if kwargs.get("price_old"):
            select_values.append(Book.price_old == kwargs.get("price_old"))
        if kwargs.get("discount"):
            select_values.append(Book.discount == kwargs.get("discount"))
        if kwargs.get("rating"):
            select_values.append(Book.rating == kwargs.get("rating"))

        stmt = select(Book).where(and_(*select_values))
        fetched_books = await self.async_session.execute(stmt)
        return (
            fetched_books.scalars().first()
            if kwargs.get("book_id") or kwargs.get("book_num") is not None
            else fetched_books.scalars().all()
        )


class Paginate:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def select_books(
        self, page: int, books_quantity: int, sort_by: SortChoices, order_asc: bool
    ) -> Sequence[Book]:
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = (
            getattr(Book, sort_by.value) if hasattr(Book, sort_by.value) else Book.title
        )
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        stmt = (
            select(Book).limit(books_quantity).offset(books_offset).order_by(sort_order)
        )
        result = await self.async_session.execute(stmt)
        return result.scalars().all()


class InsertBook(BaseRepository):
    async def insert_new_book(self, new_book: dict) -> Book | None:
        current_book = await self.select_book(book_num=new_book.get("book_num"))
        if current_book is None:
            new_book = Book(
                book_num=new_book.get("book_num"),
                title=new_book.get("title"),
                author=new_book.get("author"),
                price_new=new_book.get("price_new"),
                price_old=new_book.get("price_old"),
                discount=new_book.get("discount"),
                rating=new_book.get("rating"),
                image=new_book.get("image_url"),
            )
            self.async_session.add(new_book)
            await self.async_session.flush([new_book])
            await self.async_session.refresh(new_book)
            return new_book
        else:
            return None


class UpdateBook(BaseRepository):
    async def update_book(self, book: dict) -> Book | None:
        current_book = await self.select_book(book_num=book.get("book_num"))

        if current_book is not None:
            update_values = {
                "title": book.get("title"),
                "author": book.get("author"),
                "rating": book.get("rating"),
                "image": book.get("image_url"),
            }

            new_price = book.get("price_new")
            if new_price is not None:
                new_price = float(new_price)
                old_price = float(current_book.price_new)
                update_values["price_new"] = new_price
                update_values["price_old"] = old_price
                update_values["discount"] = (
                    f"{round(((old_price - new_price) / old_price * 100))}%"
                )

            stmt = (
                update(Book)
                .where(Book.book_num == book.get("book_num"))
                .values(**update_values)
            )
            await self.async_session.execute(stmt)
            await self.async_session.refresh(current_book)
            return current_book
        else:
            return None


class DeleteBook(BaseRepository):

    async def delete_book(self, **kwargs) -> Book | None:
        deleted_book = await self.select_book(**kwargs)
        select_values = list()
        if kwargs.get("book_id"):
            select_values.append(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            select_values.append(Book.book_num == kwargs.get("book_num"))

        stmt = delete(Book).where(*select_values)
        await self.async_session.execute(stmt)

        return deleted_book
