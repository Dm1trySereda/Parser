from abc import ABC, abstractmethod

from src.models.users import User


class AbstractGetUserService(ABC):
    @abstractmethod
    async def get_current_user(self, email: str = None, remote_user_id: int = None,
                               username: str = None) -> User | None:
        pass
