from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status, Body
from fastapi.security import OAuth2PasswordRequestForm

from src.services.auth_services.auth_user import authenticate_user, create_access_token, get_current_active_user
from src.services.auth_services.repository import RepositoryGetCurrentUserService, AbstractGetCurrentUserService
from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import Token, UserResponse
from src.request_shemas.users import UserRequest
from src.validation.book_validates import validate_inserter

user_routes = APIRouter(tags=["Users"])


@user_routes.post("/login")
async def login(
        request: Request, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await authenticate_user(request, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings_auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@user_routes.get("/users/me")
async def read_users_me(
        current_user: Annotated[UserResponse, Depends(get_current_active_user)]
):
    return current_user


@user_routes.post("/registration", status_code=status.HTTP_201_CREATED,
                  response_model=UserResponse,
                  response_description="User created", )
async def registration(request: Request, new_user: Annotated[UserRequest, Body(embed=False)]):
    user_inserter: AbstractGetCurrentUserService = RepositoryGetCurrentUserService(request.state.db)
    new_user = await user_inserter.create_user(new_user)
    try:
        validate_inserter(new_user)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return new_user
