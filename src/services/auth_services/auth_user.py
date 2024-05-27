from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import (TokenData, UserInDBResponse,
                                        UserResponse)
from src.services.auth_services.repository import (
    AbstractGetCurrentUserService, RepositoryGetCurrentUserService)

oauth2_scheme = HTTPBearer()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Hash the password
def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Creating a JWT token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode, settings_auth.SIGNATURE, algorithm=settings_auth.ALGORITHM
    )
    return encode_jwt


# Checks the token and returns the user if it exists
async def get_current_user(
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
    user = get_user(request=request, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# Checks if the user is active
async def get_current_active_user(
        current_user: Annotated[UserResponse, Depends(get_current_user)],
):
    current_user = await current_user
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# Getting a user from the  db
async def get_user(request: Request, username: str):
    user: AbstractGetCurrentUserService = RepositoryGetCurrentUserService(
        request.state.db
    )
    user_dict = await user.get_current_user(username=username)
    if user_dict:
        return UserInDBResponse(**user_dict.__dict__)


# Authentication user
async def authenticate_user(request: Request, username: str, password: str):
    user: UserInDBResponse = await get_user(request=request, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
