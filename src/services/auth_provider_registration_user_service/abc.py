from abc import ABC, abstractmethod

from src.request_shemas.users import RemoteUserInfoRequest


class AbstractAuthProviderRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_auth_provider(
        self, user: RemoteUserInfoRequest, provider: str
    ):
        pass
