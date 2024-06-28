from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.history import SearchHistory
from src.response_schemas.history import HistoryOut
from src.services.search_history_service.abc import AbstractSearchHistoryService


class RepositorySearchHistoryService(AbstractSearchHistoryService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SearchHistory(session)

    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
    ) -> list[HistoryOut]:
        history = await self.repository.select_history(
            book_id=book_id, book_num=book_num, title=title, author=author
        )
        return TypeAdapter(list[HistoryOut]).validate_python(history)
