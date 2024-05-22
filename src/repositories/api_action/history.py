from fastapi import HTTPException, status
from sqlalchemy import and_, func, select

from src.models.history import History


class BaseRepository:
    def __init__(self, session):
        self.async_session = session


class SearchHistory(BaseRepository):

    async def select_book_history(
        self, book_id: int = None, book_num: int = None, title: str = None
    ) -> History:
        select_values = list()

        if book_id:
            select_values.append(History.book_id == book_id)
        if book_num:
            select_values.append(History.book_num == book_num)
        if title:
            select_values.append(History.title.startswith(title))
        if not select_values:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        stmt = select(History).where(and_(*select_values))
        fetched_books = await self.async_session.execute(stmt)
        books_history = fetched_books.scalars().all()
        if len(books_history) <= 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="History not found"
            )
        return books_history


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
