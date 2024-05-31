from typing import Annotated

import jwt
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
    try:
        payload = jwt.decode(
            token.credentials,
            settings_auth.SIGNATURE,
            algorithms=[settings_auth.ALGORITHM],
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except InvalidTokenError:
        raise credentials_exception
    searcher: AbstractGeUserInDbService = RepositoryGetUserService(request.state.db)
    user = await searcher.get_current_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def verify_user_is_active(
        current_user: Annotated[UserResponse, Depends(verify_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user
