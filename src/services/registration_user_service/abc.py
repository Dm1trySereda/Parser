from abc import ABC, abstractmethod

from src.request_shemas.users import RemoteUserInfoRequest, UserRequest


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(
        self, new_user: UserRequest | RemoteUserInfoRequest, confirmation_code: int
    ):
        pass
