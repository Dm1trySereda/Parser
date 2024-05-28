from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


class AbstractPaginateBookService(ABC):
    @abstractmethod
    async def paginate(self, **kwargs) -> list[BookOuts]:
        pass
