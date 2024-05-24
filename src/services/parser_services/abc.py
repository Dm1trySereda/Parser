from abc import ABC, abstractmethod
from src.models.books import Book


class AbstractParserBookService(ABC):
    @abstractmethod
    async def check_book(self, **kwargs: dict) -> Book | None:
        pass

    @abstractmethod
    async def delete_duplicate(self):
        pass

    @abstractmethod
    async def add_new_book(self, new_book: dict) -> Book:
        pass

    @abstractmethod
    async def update_book(self, current_book, book: dict) -> Book:
        pass
