from datetime import timedelta

from fastapi import HTTPException, status

from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import Token, RemoteToken
from src.services.auth_services.abc import AbstractAuthUserService
from src.services.create_token_service.abc import AbstractCreateTokenService
from src.services.get_remote_token_service.abc import AbstractGetRemoteTokenService


class AuthenticateUserFacade:
    def __init__(
            self,
            auth_service: AbstractAuthUserService,
            create_token_service: AbstractCreateTokenService,
            get_remote_token_service: AbstractGetRemoteTokenService,
            # get_user_service: AbstractGetUserService,
            # create_user_service: AbstractCreateUserService,
    ):
        # self.get_user_service = get_user_service
        # self.create_user_service = create_user_service
        self.get_remote_token_service = get_remote_token_service
        self.auth_service = auth_service
        self.create_token_service = create_token_service

    async def authentication(self, form_data):
        user = await self.auth_service.authenticate_user(
            username=form_data.username, password=form_data.password
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
        return Token(access_token=access_token, token_type="Bearer")

    async def authentication_with_code(self, code, provider):
        # тут же добавить регистрацию пользователя
        # access_token = await self.get_remote_token_service.get_token(code=code)
        # remote_id = ...
        # user = await self.get_user_service.get(provider=provider, remote_user_id=remote_id)
        # if not user:
        #     user = await self.create_user_service.create(auth_provider_informations=[AuthProviderInfo(remote_id=remote_id, provider=provider, )])
        #
        # return GoogleToken(access_token=access_token, token_type="Bearer")

        access_token = await self.get_remote_token_service.get_token(code=code)
        return RemoteToken(access_token=access_token, token_type="Bearer", provider=provider)
