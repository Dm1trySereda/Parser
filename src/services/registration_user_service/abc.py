from abc import ABC, abstractmethod

from src.request_shemas.users import GoogleUserRequest, UserRequest


class AbstractRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_user(self, new_user: UserRequest | GoogleUserRequest):
        pass
