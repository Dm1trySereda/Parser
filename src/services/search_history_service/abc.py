from abc import ABC, abstractmethod
from src.response_schemas.history import HistoryOut


class AbstractSearchHistoryService(ABC):
    @abstractmethod
    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
    ) -> list[HistoryOut]:
        pass
