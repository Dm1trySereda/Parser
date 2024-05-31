from abc import ABC, abstractmethod

from fastapi import Request

from src.response_schemas.users import UserInDBResponse


class AbstractAuthUserService(ABC):

    @abstractmethod
    async def authenticate_user(self, username: str, password: str):
        pass
