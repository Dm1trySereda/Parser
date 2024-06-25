from abc import ABC, abstractmethod

from src.models import Book


class AbstractDeleteBookService(ABC):
    @abstractmethod
    async def delete_book(
        self, current_book: Book, book_id: int = None, book_num: int = None
    ) -> Book:
        pass
