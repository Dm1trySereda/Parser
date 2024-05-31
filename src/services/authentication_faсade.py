from datetime import timedelta

from fastapi import HTTPException, status

from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import Token
from src.services.auth_services.abc import AbstractAuthUserService
from src.services.create_token_service.abc import AbstractCreateTokenService


class AuthenticateUserFacade:
    def __init__(
            self,
            auth_service: AbstractAuthUserService,
            create_token_service: AbstractCreateTokenService,
    ):
        self.auth_service = auth_service
        self.create_token_service = create_token_service

    async def authentication(self, form_data):
        user = await self.auth_service.authenticate_user(
            form_data.username, form_data.password
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(
            minutes=settings_auth.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = await self.create_token_service.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer")
