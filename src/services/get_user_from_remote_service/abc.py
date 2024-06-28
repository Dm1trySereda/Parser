from abc import ABC, abstractmethod

from src.response_schemas.users import RemoteUserInfoResponse
from src.response_schemas.users import RemoteToken


class AbstractGetUserInfoFromRemoteService(ABC):
    @abstractmethod
    async def get_user_info(self, remote_token: RemoteToken) -> RemoteUserInfoResponse:
        pass
