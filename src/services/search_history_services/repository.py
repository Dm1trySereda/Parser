from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import History
from src.repository.api_action.history import SearchHistory
from src.services.search_history_services.abc import AbstractSearchHistoryService


class RepositorySearchHistoryService(AbstractSearchHistoryService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def search(self, **kwargs) -> History | Sequence[History] | None:
        searcher = SearchHistory(self.session)
        return await searcher.select_history(**kwargs)
