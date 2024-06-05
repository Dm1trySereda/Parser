from abc import ABC, abstractmethod

from src.models.users import BaseUser


class AbstractGeUserInDbService(ABC):
    @abstractmethod
    async def get_current_user(self, username: str) -> BaseUser:
        pass
