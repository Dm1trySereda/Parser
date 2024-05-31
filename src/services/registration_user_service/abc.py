from abc import ABC, abstractmethod

from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(self, new_user: UserRequest):
        pass
