from abc import ABC, abstractmethod

from src.models import History


class AbstractBookPriceAlertService(ABC):
    @abstractmethod
    async def get_price(self) -> list[History]:
        pass
