from abc import ABC, abstractmethod
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

oauth2_scheme = HTTPBearer()


class AbstractValidateTokenService(ABC):
    @abstractmethod
    async def validate_token_service(
        self, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]
    ):
        pass
