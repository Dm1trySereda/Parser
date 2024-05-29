from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


class AbstractSearchBookService(ABC):
    @abstractmethod
    async def search(self, **kwargs) -> list[BookOuts]:
        pass
