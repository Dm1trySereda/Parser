from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import SelectBook
from src.services.search_book_services.abc import AbstractSearchBookService


class RepositorySearchBookService(AbstractSearchBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, **kwargs) -> Book | Sequence[Book] | None:
        searcher = SelectBook(self.session)
        fetched_books = await searcher.select_book(**kwargs)
        return (
            fetched_books.scalar_one_or_none()
            if kwargs.get("book_id") or kwargs.get("book_num") is not None
            else fetched_books.scalars().all()
        )
