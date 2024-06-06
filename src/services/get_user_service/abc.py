from abc import ABC, abstractmethod

from src.models.users import User


class AbstractGeUserService(ABC):
    @abstractmethod
    async def get_current_user(self, username: str) -> User | None:
        pass
