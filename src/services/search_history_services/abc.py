from abc import ABC, abstractmethod

from src.response_schemas.history import HistoryOut


class AbstractSearchHistoryService(ABC):
    @abstractmethod
    async def search(self, **kwargs) -> HistoryOut | list[HistoryOut]:
        pass
