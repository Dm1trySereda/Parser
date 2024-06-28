from abc import ABC, abstractmethod
from src.response_schemas.users import UserResponse


class AbstractAuthUserService(ABC):

    @abstractmethod
    async def authenticate_user(
        self, username: str, password: str
    ) -> UserResponse | None:
        pass
