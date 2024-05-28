from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import Book
from src.repository.books import SelectBook
from src.services.search_book_services.abc import AbstractSearchBookService


class RepositorySearchBookService(AbstractSearchBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher = SelectBook(session)

    async def search(self, **kwargs) -> Sequence[Book] | None:
        fetched_books = await self.searcher.select_book(**kwargs)
        return fetched_books.scalars().all()
