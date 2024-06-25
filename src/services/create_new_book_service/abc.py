from abc import ABC, abstractmethod

from src.models import Book
from src.request_shemas.books import BookIn


class AbstractAddNewBookService(ABC):
    @abstractmethod
    async def add_new_book(self, new_book: BookIn) -> Book:
        pass
