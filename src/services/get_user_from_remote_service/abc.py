from abc import ABC, abstractmethod

from src.request_shemas.users import RemoteUserInfoRequest
from src.response_schemas.users import RemoteToken


class AbstractGetUserInfoFromRemoteService(ABC):
    async def get_user_info(self, remote_token: RemoteToken) -> RemoteUserInfoRequest:
        pass
