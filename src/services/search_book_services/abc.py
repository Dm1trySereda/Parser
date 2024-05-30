from abc import ABC, abstractmethod

from src.response_schemas.books import BookOuts


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
    ) -> list[BookOuts]:
        pass
