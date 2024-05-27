from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


class AbstractDeleteBookService(ABC):
    @abstractmethod
    async def delete_book(self, **kwargs) -> BookOuts:
        pass