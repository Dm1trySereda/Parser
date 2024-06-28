from typing import Sequence

from sqlalchemy import and_, exists, func, insert, join, select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.history import HistorySortChoices
from src.models import History
from src.models.books import Book
from src.models.history import History


class BaseRepository:
    def __init__(self, session: AsyncSession):
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
    async def select_all_history(
        self,
        page: int,
        books_quantity: int,
        sort_by: HistorySortChoices,
        order_asc: bool,
    ) -> Sequence[History]:
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = (
            getattr(History, sort_by.value)
            if hasattr(History, sort_by.value)
            else History.price
        )
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        subquery = (
            select(History.book_num, func.count().label("count"))
            .group_by(History.book_num)
            .having(func.count() > 1)
        ).subquery()

        query = select(History)
        query = (
            query.join(
                subquery,
                History.book_num == subquery.c.book_num,
            )
            .limit(books_quantity)
            .offset(books_offset)
            .order_by(sort_order)
        )
        result = await self.async_session.execute(query)
        duplicated_books = result.scalars().all()
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
