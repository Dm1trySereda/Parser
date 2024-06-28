from abc import ABC, abstractmethod


from src.response_schemas.users import RemoteUserInfoResponse, UserResponse
from src.request_shemas.users import UserRequest


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(
        self, new_user: UserRequest | RemoteUserInfoResponse, is_active: bool = False
    ) -> UserResponse:
        pass
