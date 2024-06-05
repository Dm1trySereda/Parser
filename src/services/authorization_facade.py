from typing import Annotated

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.models.users import BaseUser
from src.services.get_user_in_db_service.repository import (
    AbstractGeUserInDbService,
    RepositoryGetUserService,
)
from src.services.validate_token.repository import (
    AbstractValidateTokenService,
    RepositoryValidateTokenService,
)

oauth2_scheme = HTTPBearer()


class AuthorizationFacade:
    def __init__(
            self,
            validate_token_service: AbstractValidateTokenService,
    ):
        self.validate_token_service = validate_token_service

    async def verify_user(
            self,
            request: Request,
            token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
    ):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

        access_token = await self.validate_token_service.validate_token(token)
        if access_token is None:
            raise credentials_exception

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

    def get_permissions_checker(self, roles: list[int]):
        async def check_permissions(user: BaseUser = Depends(self.verify_user)):
            if user.role_id not in roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )
            return user

        return check_permissions

#
# async def verify_user(request: Request,
#                       token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
#                       ):
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     validate_token: AbstractValidateTokenService = RepositoryValidateTokenService()
#     access_token = await validate_token.validate_token(token)
#     if access_token is None:
#         raise credentials_exception
#     try:
#         username: str = access_token.get("sub")
#     except AttributeError:
#         async with httpx.AsyncClient() as client:
#             response = await client.get(
#                 "https://people.googleapis.com/v1/people/me",
#                 params={"personFields": "names,emailAddresses"},
#                 headers={"Authorization": f"Bearer {access_token}"},
#             )
#             if response.status_code == status.HTTP_200_OK:
#                 profile_info = response.json()
#                 email_data = profile_info["emailAddresses"][0]
#                 username = email_data["metadata"]["source"]["id"]
#
#     user: AbstractGeUserInDbService = RepositoryGetUserService(request.state.db)
#     check_user = await user.get_current_user(username=username)
#     return check_user
#
#
# def get_permissions_checker(roles: list[int]):
#     async def check_permissions(user: BaseUser = Depends(verify_user)):
#         if user.role_id not in roles:
#             raise HTTPException(
#                 status_code=status.HTTP_403_FORBIDDEN,
#                 detail="Not enough permissions",
#             )
#         return user
#
#     return check_permissions
