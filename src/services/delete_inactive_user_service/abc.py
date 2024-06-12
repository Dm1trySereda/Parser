from abc import ABC, abstractmethod
from datetime import datetime


class AbstractDeleteInactiveUserService(ABC):
    @abstractmethod
    async def delete_inactive_user(self, current_time: datetime):
        pass
