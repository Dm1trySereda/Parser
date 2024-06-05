from abc import ABC, abstractmethod
from datetime import timedelta


class AbstractCreateTokenService(ABC):
    @abstractmethod
    async def create_access_token(
        self, data: dict, expires_delta: timedelta | None = None
    ):
        pass
