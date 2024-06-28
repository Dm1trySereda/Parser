from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


class AbstractDeleteBookService(ABC):
    @abstractmethod
    async def delete_book(
        self, existing_book: BookOuts, book_id: int = None, book_num: int = None
    ) -> BookOuts:
        pass
