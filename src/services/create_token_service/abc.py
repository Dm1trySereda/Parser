from abc import abstractmethod, ABC
from datetime import timedelta


class AbstractCreateTokenService(ABC):
    @abstractmethod
    async def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        pass
