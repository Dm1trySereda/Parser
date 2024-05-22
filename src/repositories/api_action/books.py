from typing import Sequence, List

from fastapi import HTTPException, status
from sqlalchemy import and_, asc, delete, desc, func, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.models.books import Book
from src.enums.book import SortChoices


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def select_book(
            self, book_id: int = None, book_num: int = None, title: str = None
    ):
        select_values = list()

        if book_id:
            select_values.append(Book.id == book_id)
        if book_num:
            select_values.append(Book.book_num == book_num)
        if title:
            select_values.append(Book.title.contains(title))

        stmt = select(Book).where(and_(*select_values))
        fetched_books = await self.async_session.execute(stmt)
        return (
            fetched_books.scalars().first()
            if book_id or book_num
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
        current_book = await self.select_book(new_book.get("book_num"))
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


class DeleteEntity(BaseRepository):
    def __init__(self, model, session):
        super().__init__(session)
        self.model = model

    async def delete(self, **kwargs):
        stmt = delete(self.model).filter_by(
            **{key: value for key, value in kwargs.items() if value}
        )
        current_book = await self.async_session.execute(stmt)
        return current_book


class DeleteBook(DeleteEntity):
    def __init__(self, session):
        super().__init__(Book, session)

    async def delete_book(self, book_id=None, book_num=None) -> Book | None:
        deleted_book = await self.select_book(book_id=book_id, book_num=book_num)
        select_values = list()
        if book_id:
            select_values.append(Book.id == book_id)
        if book_num:
            select_values.append(Book.book_num == book_num)

        await self.delete(book_id=book_id, book_num=book_num)

        return deleted_book if deleted_book is not None else None
