from abc import ABC, abstractmethod

from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts


class AbstractAddNewBookService(ABC):
    @abstractmethod
    async def add_new_book(self, new_book: BookIn) -> BookOuts:
        pass
