from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.history import History
from src.repository.history import SearchHistory
from src.services.search_history_service.abc import \
    AbstractSearchHistoryService


class RepositorySearchHistoryService(AbstractSearchHistoryService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.history_searcher = SearchHistory(session)

    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
    ) -> Sequence[History]:
        return await self.history_searcher.select_history(
            book_id=book_id, book_num=book_num, title=title, author=author
        )
