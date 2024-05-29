from abc import ABC, abstractmethod

from src.response_schemas.users import UserInDBResponse, UserResponse


class AbstractGetCurrentUserService(ABC):
    @abstractmethod
    async def get_current_user(self, username: str) -> UserInDBResponse:
        pass

    @abstractmethod
    async def create_user(self, new_user: dict) -> UserResponse:
        pass
