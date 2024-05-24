from abc import ABC, abstractmethod
from src.models.books import Book
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts


class AbstractUpdateBookService(ABC):
    @abstractmethod
    async def update(self, book: BookIn) -> BookOuts | None:
        pass
