from abc import ABC, abstractmethod

from src.models import Book


class AbstractSearchBookService(ABC):
    @abstractmethod
    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
    ) -> list[Book]:
        pass
