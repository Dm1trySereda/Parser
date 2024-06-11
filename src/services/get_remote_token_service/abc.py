from abc import ABC, abstractmethod

from src.response_schemas.users import RemoteToken


class AbstractGetRemoteTokenService(ABC):
    @abstractmethod
    async def get_token(self, **creds) -> RemoteToken: ...
