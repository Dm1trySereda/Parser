from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


class AbstractSearchBookService(ABC):
    @abstractmethod
    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        authors: list = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
        years: list = None,
    ) -> list[BookOuts]:
        pass

    @abstractmethod
    async def search_popular(self, count: int = 10):
        pass

    @abstractmethod
    async def search_publishing_year(self, count: int = 10):
        pass
