from abc import ABC, abstractmethod

from src.models.users import User


class AbstractAuthUserService(ABC):

    @abstractmethod
    async def authenticate_user(self, username: str, password: str) -> User | None:
        pass
