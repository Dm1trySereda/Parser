from abc import ABC, abstractmethod

from src.response_schemas.users import UserInDBResponse


class AbstractGeUserInDbService(ABC):
    @abstractmethod
    async def get_current_user(self, username: str) -> UserInDBResponse:
        pass
