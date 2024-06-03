from typing import Annotated

from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security import HTTPBasicCredentials
from jwt import InvalidTokenError
from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserInDBResponse, UserResponse, TokenData
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import verify_user
from src.services.create_token_service.repository import \
    RepositoryCreateTokenService
from src.services.get_user_in_db_service.abc import AbstractGeUserInDbService
from src.services.get_user_in_db_service.repository import \
    RepositoryGetUserService
from src.services.registration_user_faсade import RegistrationUserFacade
from src.services.registration_user_service.repository import \
    RepositoryRegistrationUserService

user_routes = APIRouter(tags=["Users"])


@user_routes.post("/authentication")
async def login(
        request: Request, form_data: Annotated[HTTPBasicCredentials, Depends()]
):
    auth_facade = AuthenticateUserFacade(
        auth_service=RepositoryAuthUserService(request.state.db),
        create_token_service=RepositoryCreateTokenService(),
    )
    return await auth_facade.authentication(form_data)


@user_routes.post(
    "/registration",
    status_code=status.HTTP_201_CREATED,
    response_model=UserInDBResponse,
    response_description="User created",
)
async def registration(request: Request, new_user: Annotated[UserRequest, Depends()]):
    regis_facade = RegistrationUserFacade(
        search_services=RepositoryGetUserService(request.state.db),
        registration_services=RepositoryRegistrationUserService(request.state.db),
    )

    return await regis_facade.registration_user(new_user)


@user_routes.get(
    "/users/about_me", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def read_users_me(
        token: Annotated[UserResponse, Depends(verify_user)], request: Request
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        username: str = token.get("sub")

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username)

    except InvalidTokenError:
        raise credentials_exception

    searcher: AbstractGeUserInDbService = RepositoryGetUserService(request.state.db)
    user = await searcher.get_current_user(username=token_data.username)

    if user is None:
        raise credentials_exception
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )

    return user
