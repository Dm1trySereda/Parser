from typing import Sequence

from sqlalchemy import and_, func, join, select, insert, exists

from src.models.books import Book
from src.models.history import History


class BaseRepository:
    def __init__(self, session):
        self.async_session = session


class SearchHistory(BaseRepository):

    async def select_history(self, **kwargs) -> History | Sequence[History] | None:

        select_values = list()

        if kwargs.get("book_id"):
            select_values.append(History.book_id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            select_values.append(History.book_num == kwargs.get("book_num"))
        if kwargs.get("title"):
            select_values.append(History.title.contains(kwargs.get("title")))
        if kwargs.get("price"):
            select_values.append(History.price == kwargs.get("price"))
        if kwargs.get("author"):
            stmt = (
                select(History)
                .select_from(join(History, Book, History.book_id == Book.id))
                .where(
                    (Book.author.contains(kwargs.get("author")))
                    & (and_(*select_values))
                )
            )
            fetched_books = await self.async_session.execute(stmt)
            return fetched_books.scalars().all()

        stmt = select(History).where(and_(*select_values))
        fetched_books = await self.async_session.execute(stmt)
        return fetched_books.scalars().all()


class RepetitiveBook(BaseRepository):
    async def select_all_history(self):
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


class UpdateHistory(BaseRepository):
    async def update_books_history(self):
        stmt = insert(History).from_select(
            ["book_id", "created_at", "updated_at", "book_num", "title", "price"],
            select(
                Book.id,
                Book.created_at,
                Book.updated_at,
                Book.book_num,
                Book.title,
                Book.price_new,
            ).where(
                ~exists()
                .where(History.book_num == Book.book_num)
                .where(History.price == Book.price_new)
            ),
        )

        await self.async_session.execute(stmt)
        await self.async_session.commit()
