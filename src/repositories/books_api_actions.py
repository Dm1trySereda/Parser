from typing import Sequence

from sqlalchemy import and_, asc, delete, desc, func, select, update

from src.models.books import Book
from src.models.history import History


class BaseRepository:
    def __init__(self, session):
        self.async_session = session


class DeleteEntity(BaseRepository):
    def __init__(self, model, session):
        super().__init__(session)
        self.model = model

    async def delete(self, **kwargs):
        delete_values = [
            getattr(self.model, key) == value
            for key, value in kwargs.items()
            if value is not None
        ]
        stmt = delete(self.model).where(and_(*delete_values))
        await self.async_session.execute(stmt)


class SearchBook(BaseRepository):

    async def select_book(
            self, book_id: int, book_num: int, title: str
    ) -> Sequence[Book]:
        select_values = list()

        if book_id:
            select_values.append(Book.id == book_id)
        if book_num:
            select_values.append(Book.book_num == book_num)
        if title:
            select_values.append(Book.title.contains(title))

        stmt = select(Book).where(and_(*select_values))
        result = await self.async_session.execute(stmt)

        return result.scalars().all()


class UpdateBook(BaseRepository):
    async def update_book(self, book: dict) -> None:
        current_book = select(Book.price_new).where(
            Book.book_num == book.get("book_num")
        )
        result = await self.async_session.execute(current_book)
        current_book_old = result.scalars().first()

        update_values = {
            "title": book.get("title"),
            "author": book.get("author"),
            "rating": book.get("rating"),
            "image": book.get("image"),
        }

        new_price = book.get("price")
        if new_price is not None:
            update_values["price_new"] = new_price
            update_values["price_old"] = current_book_old
            update_values["discount"] = (
                    str(
                        round(
                            (float(current_book_old) - new_price)
                            / float(current_book_old) * 100,
                            2,
                        )
                    )
                    + "%"
            )

        # Очистка словаря от значений None
        update_values = {k: v for k, v in update_values.items() if v is not None}

        stmt = (
            update(Book)
            .where(Book.book_num == book.get("book_num"))
            .values(**update_values)
        )
        await self.async_session.execute(stmt)


class InsertBook(BaseRepository):
    async def insert_new_book(self, new_book: dict) -> None:
        stmt = select(Book).where(Book.book_num == new_book.get("book_num"))
        result = await self.async_session.execute(stmt)
        existing_book = result.scalars().first()
        if existing_book is None:
            new_book = Book(
                book_num=new_book.get("book_num"),
                title=new_book.get("title"),
                author=new_book.get("author"),
                price_new=new_book.get("price"),
                rating=new_book.get("rating"),
                image=new_book.get("image"),
            )
            self.async_session.add(new_book)
        else:
            book_updater = UpdateBook(self.async_session)
            await book_updater.update_book(book=new_book)


class DeleteBook(DeleteEntity):
    def __init__(self, session):
        super().__init__(Book, session)


class DeleteHistory(DeleteEntity):
    def __init__(self, session):
        super().__init__(History, session)

    async def delete_history(self, book_id=None, book_num=None):
        await self.delete(book_id=book_id, book_num=book_num)

        book_deleter = DeleteBook(self.async_session)
        await book_deleter.delete(id=book_id, book_num=book_num)


class Paginate(BaseRepository):
    async def select_books(
            self, page: int, books_quantity: int, sort_by: str, order_asc: bool
    ) -> Sequence[Book]:
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = getattr(Book, sort_by) if hasattr(Book, sort_by) else Book.title
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        stmt = (
            select(Book).limit(books_quantity).offset(books_offset).order_by(sort_order)
        )
        result = await self.async_session.execute(stmt)
        return result.scalars().all()


class RepetitiveBook(BaseRepository):
    async def select_book_history(self):
        stmt = (
            select(History.book_num)
            .group_by(History.book_num)
            .having(func.count(History.book_num) > 1)
        )
        result = await self.async_session.execute(stmt)

        duplicate_book_nums = result.scalars().all()
        duplicated_books = list()
        for book_num in duplicate_book_nums:
            stmt = select(History).where(History.book_num == book_num)
            result = await self.async_session.execute(stmt)
            duplicated_books.extend(result.scalars().all())

        return duplicated_books
