from abc import abstractmethod, ABC
from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

oauth2_scheme = HTTPBearer()


class AbstractValidateTokenService(ABC):
    @abstractmethod
    async def validate_token(self, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]):
        pass
