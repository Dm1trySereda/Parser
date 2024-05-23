from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import BaseRepository
from src.services.search_book_services.abc import AbstractSearchBookService


class RepositorySearchBookService(AbstractSearchBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, **kwargs) -> Book | Sequence[Book] | None:
        searcher = BaseRepository(self.session)
        return await searcher.select_book(**kwargs)
