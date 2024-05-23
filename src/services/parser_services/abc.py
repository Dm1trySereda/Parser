from abc import ABC, abstractmethod
from src.models.books import Book


class AbstractParserBookService(ABC):
    @abstractmethod
    async def add_new_book(self, new_book: dict) -> Book:
        pass

    @abstractmethod
    async def update_book(self, new_book: dict) -> Book:
        pass
