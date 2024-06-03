from typing import Annotated

import jwt
import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import TokenData, UserResponse
from src.services.get_user_in_db_service.repository import (
    AbstractGeUserInDbService,
    RepositoryGetUserService,
)

oauth2_scheme = HTTPBearer()


async def verify_user(
        request: Request,
        token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    google_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/tokeninfo",
        params={"access_token": token.credentials},
    )
    if google_response.status_code == status.HTTP_200_OK:
        return token.credentials
    else:

        payload = jwt.decode(
            token.credentials,
            settings_auth.SIGNATURE,
            algorithms=[settings_auth.ALGORITHM],
        )
        return payload


async def verify_user_is_active(
        current_user: Annotated[UserResponse, Depends(verify_user)],
):
    if type(current_user) == UserResponse:
        if not current_user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return current_user
