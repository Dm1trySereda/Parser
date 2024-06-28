from abc import ABC, abstractmethod

from src.enums.history import HistorySortChoices
from src.response_schemas.history import HistoryOut


class AbstractBookPriceAlertService(ABC):
    @abstractmethod
    async def get_price(
        self,
        page: int,
        books_quantity: int,
        sort_by: HistorySortChoices,
        order_asc: bool,
    ) -> list[HistoryOut]:
        pass
