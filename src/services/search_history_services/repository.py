from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import History
from src.repository.history import SearchHistory
from src.services.search_history_services.abc import AbstractSearchHistoryService


class RepositorySearchHistoryService(AbstractSearchHistoryService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.history_searcher = SearchHistory(session)

    async def search(self, **kwargs) -> History | Sequence[History] | None:
        return await self.history_searcher.select_history(**kwargs)
