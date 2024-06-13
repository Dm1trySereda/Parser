from abc import ABC, abstractmethod

from src.request_shemas.users import RemoteUserInfoRequest, UserRequest
from src.response_schemas.users import UserResponse


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(
        self, new_user: UserRequest | RemoteUserInfoRequest, is_active: bool = False
    ) -> UserResponse:
        pass
