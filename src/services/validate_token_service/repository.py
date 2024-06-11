from typing import Annotated

import httpx
import jwt
from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials
from jwt import InvalidTokenError

from src.config.auth_provider.auth_provider_config import settings_auth
from src.services.validate_token_service.abc import (
    AbstractValidateTokenService,
    oauth2_scheme,
)


class RepositoryValidateTokenService(AbstractValidateTokenService):

    async def validate_token_service(
        self, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]
    ):
        access_token = token.credentials
        try:
            access_token_decode = jwt.decode(
                access_token,
                settings_auth.SIGNATURE,
                algorithms=[settings_auth.ALGORITHM],
            )
            return access_token_decode
        except InvalidTokenError:
            async with httpx.AsyncClient() as client:
                google_response = await client.get(
                    "https://www.googleapis.com/oauth2/v1/tokeninfo",
                    params={"access_token": access_token},
                )
                if google_response.status_code == status.HTTP_200_OK:
                    return access_token
                else:
                    return None
