from abc import ABC, abstractmethod

from src.response_schemas.history import HistoryOut


class AbstractBookPriceAlertService(ABC):
    @abstractmethod
    async def get_price(
            self
    ) -> list[HistoryOut]:
        pass
