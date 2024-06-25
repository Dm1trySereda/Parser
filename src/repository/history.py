from sqlalchemy import and_, exists, func, insert, join, select

from src.models.books import Book
from src.models.history import History


class BaseRepository:
    def __init__(self, session):
        self.async_session = session


class SearchHistory(BaseRepository):

    async def select_history(self, **kwargs) -> list[History] | None:
        subquery = (
            select(History.book_id, func.count(History.book_id).label("count"))
            .group_by(History.book_id)
            .alias("book_counts")
        )

        query = (
            select(History, Book.author, subquery.c.count)
            .outerjoin(Book, History.book_id == Book.id)
            .outerjoin(subquery, History.book_id == subquery.c.book_id)
        )

        if kwargs.get("book_id"):
            query = query.where(History.book_id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            query = query.where(History.book_num == kwargs.get("book_num"))
        if kwargs.get("title"):
            query = query.where(History.title.contains(kwargs.get("title")))
        if kwargs.get("author"):
            query = query.where(
                and_(Book.author.contains(kwargs.get("author")), subquery.c.count > 1)
            )
        res = await self.async_session.stream(query)
        fetched_books = [row.History for row in await res.all()]

        return fetched_books


class RepetitiveBook(BaseRepository):
    async def select_all_history(self) -> list[History]:
        subquery = (
            select(History.book_num)
            .group_by(History.book_num)
            .having(func.count(History.book_num) > 1)
        )
        result = await self.async_session.execute(subquery)

        duplicate_book_nums = result.scalars().all()
        duplicated_books = list()
        for book_num in duplicate_book_nums:
            query = select(History).where(History.book_num == book_num)
            result = await self.async_session.execute(query)
            duplicated_books.extend(result.scalars().all())

        return duplicated_books


class UpdateHistory(BaseRepository):
    async def update_books_history(self):
        query = insert(History).from_select(
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

        await self.async_session.execute(query)
        await self.async_session.commit()
