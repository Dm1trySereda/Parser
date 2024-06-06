from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.security import HTTPBasicCredentials

from src.config.auth.auth_config import settings_auth
from src.enums.role import UserRoleEnum
from src.models.users import User
from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.create_token_service.repository import LocalCreateTokenService
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_faсade import RegistrationUserFacade
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)
from src.services.validate_token.repository import RepositoryValidateTokenService

user_routes = APIRouter(tags=["Users"])


@user_routes.post("/authentication")
async def login(
        request: Request, form_data: Annotated[HTTPBasicCredentials, Depends()]
):
    authenticate_facade = AuthenticateUserFacade(
        auth_service=RepositoryAuthUserService(request.state.db),
        create_token_service=LocalCreateTokenService(),
        get_remote_token_service=GetGoogleTokenService(
            google_client_id=settings_auth.GOOGLE_CLIENT_ID,
            google_client_secret=settings_auth.GOOGLE_CLIENT_SECRET,
            google_redirect_url=settings_auth.GOOGLE_REDIRECT_URL,
        ))
    return await authenticate_facade.authentication(form_data)


@user_routes.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=UserResponse,
    response_description="User created",
)
async def registration(request: Request, new_user: Annotated[UserRequest, Depends()]):
    regis_facade = RegistrationUserFacade(
        search_services=RepositoryGetUserService(request.state.db),
        registration_services=RepositoryRegistrationUserService(request.state.db),
    )

    return await regis_facade.registration_user(new_user)


auth_facade = AuthorizationFacade(
    validate_token_service=RepositoryValidateTokenService()
)


@user_routes.get(
    "/users/about_me", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def about_me(
        user: User = Depends(
            auth_facade.get_permissions_checker(
                roles=[UserRoleEnum.admin, UserRoleEnum.subadmin, UserRoleEnum.client]
            )
        )
):
    return user
