from abc import ABC, abstractmethod
from src.response_schemas.users import UserResponse


class AbstractGetUserService(ABC):
    @abstractmethod
    async def get_current_user(
        self, email: str = None, remote_user_id: int = None, username: str = None
    ) -> UserResponse | None:
        pass
