from abc import ABC, abstractmethod

from src.models.users import User
from src.request_shemas.users import RemoteUserInfoRequest, UserRequest


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(
        self, new_user: UserRequest | RemoteUserInfoRequest, is_active: bool = False
    ) -> User:
        pass
