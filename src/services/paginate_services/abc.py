from abc import ABC, abstractmethod

from src.enums.book import SortChoices
from src.response_schemas.books import BookOuts


class AbstractPaginateBookService(ABC):
    @abstractmethod
    async def paginate(
            self,
            page: int = None,
            books_quantity: int = None,
            sort_by: SortChoices = None,
            order_asc: bool = None,
    ) -> list[BookOuts]:
        pass
