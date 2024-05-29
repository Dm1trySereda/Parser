from abc import ABC, abstractmethod


class AbstractUpdateHistoryService(ABC):
    @abstractmethod
    async def update_history(self):
        pass
