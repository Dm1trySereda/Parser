from typing import Annotated

import httpx
import jwt
import requests
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import DecodeError, InvalidTokenError
from src.models.users import BaseUser
from src.config.auth.auth_config import settings_auth
from src.services.get_user_in_db_service.abc import AbstractGeUserInDbService
from src.services.get_user_in_db_service.repository import RepositoryGetUserService

oauth2_scheme = HTTPBearer()


async def verify_user(
        request: Request,
        token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]
):
    check_user = await get_user_from_token(request, token)
    return check_user


async def admin(user: BaseUser = Depends(verify_user)):
    if user.role_id != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return True


async def subadmin(user: BaseUser = Depends(verify_user)):
    if user.role_id not in [1, 2]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return True


async def client(user: BaseUser = Depends(verify_user)):
    if user.role_id not in [1, 2, 3]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return True


async def check_token(token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    if not token:
        raise credentials_exception
    access_token = token.credentials
    try:
        access_token_decode = jwt.decode(
            access_token,
            settings_auth.SIGNATURE,
            algorithms=[settings_auth.ALGORITHM],
        )
        return access_token_decode
    except InvalidTokenError:
        google_response = requests.get(
            "https://www.googleapis.com/oauth2/v1/tokeninfo",
            params={"access_token": access_token},
        )
        if google_response.status_code == status.HTTP_200_OK:
            return access_token
        else:
            raise credentials_exception


async def get_user_from_token(request: Request, token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)]):
    access_token = await check_token(token)
    try:
        username: str = access_token.get("sub")
    except AttributeError:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://people.googleapis.com/v1/people/me",
                params={"personFields": "names,emailAddresses"},
                headers={"Authorization": f"Bearer {access_token}"},
            )
            if response.status_code == status.HTTP_200_OK:
                profile_info = response.json()
                email_data = profile_info["emailAddresses"][0]
                username = email_data["metadata"]["source"]["id"]

    user: AbstractGeUserInDbService = RepositoryGetUserService(request.state.db)
    check_user = await user.get_current_user(username=username)
    return check_user
