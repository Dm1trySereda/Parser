from abc import ABC, abstractmethod

from src.response_schemas.users import RemoteUserInfoResponse


class AbstractAuthProviderRegistrationUserService(ABC):
    @abstractmethod
    async def create_new_auth_provider(
        self, user: RemoteUserInfoResponse, provider: str
    ):
        pass
