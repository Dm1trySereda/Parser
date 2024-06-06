from typing import Annotated, Dict

import httpx
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.enums.role import UserRoleEnum
from src.models.users import Role, User
from src.services.get_user_service.repository import (
    AbstractGeUserService,
    RepositoryGetUserService,
)
from src.services.role_association_service.repository import (
    AbstractRoleAssociationService,
    RepositoryRoleAssociationService,
)
from src.services.validate_token.repository import AbstractValidateTokenService

oauth2_scheme = HTTPBearer()


async def get_user_service_factory(request: Request) -> AbstractGeUserService:
    return RepositoryGetUserService(request.state.db)


get_user_service_dependency = Annotated[
    AbstractGeUserService, Depends(get_user_service_factory)
]


async def get_role_association__factory(
    request: Request,
) -> AbstractRoleAssociationService:
    role_association = RepositoryRoleAssociationService(request.state.db)
    return await role_association.get_role_association()


class AuthorizationFacade:
    def __init__(
        self,
        validate_token_service: AbstractValidateTokenService,
    ):
        self.validate_token_service = validate_token_service

    async def verify_user(
        self,
        token: Annotated[HTTPAuthorizationCredentials, Depends(oauth2_scheme)],
        search_user_service: get_user_service_dependency,
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
            user = await search_user_service.get_current_user(username)
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
                    user = await search_user_service.get_current_user(username=username)
        if user is None:
            raise credentials_exception

        return user

    def get_permissions_checker(self, roles: list[UserRoleEnum]):
        async def check_permissions(
            user: User = Depends(self.verify_user),
            role_association=Depends(get_role_association__factory),
        ):
            if role_association.get(user.role_id) not in [role.value for role in roles]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Not enough permissions",
                )
            return user

        return check_permissions
