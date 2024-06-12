from datetime import timedelta

from fastapi import HTTPException, status

from src.config.auth_provider.auth_provider_config import settings_auth
from src.response_schemas.users import RemoteToken, Token
from src.services.auth_provider_registration_user_service.abc import (
    AbstractAuthProviderRegistrationUserService,
)
from src.services.auth_services.abc import AbstractAuthUserService
from src.services.create_token_service.abc import AbstractCreateTokenService
from src.services.generate_otp_code_service.abc import AbstractGenerateOtpCodeService
from src.services.get_remote_token_service.abc import AbstractGetRemoteTokenService
from src.services.get_user_from_remote_service.abc import (
    AbstractGetUserInfoFromRemoteService,
)
from src.services.get_user_service.abc import AbstractGetUserService
from src.services.registration_user_service.abc import AbstractRegistrationUserService
from src.services.send_mail_service.abc import AbstractSendMailService
from src.services.update_user_info_service.abc import AbstractUpdateUserInfoService


class AuthenticateUserFacade:
    def __init__(
        self,
        auth_service: AbstractAuthUserService,
        create_token_service: AbstractCreateTokenService,
        get_remote_token_service: AbstractGetRemoteTokenService,
        get_user_info_from_remote_service: AbstractGetUserInfoFromRemoteService,
        get_user_service: AbstractGetUserService,
        registration_user_service: AbstractRegistrationUserService,
        update_user_info_service: AbstractUpdateUserInfoService,
        auth_provider_registration_user_service: AbstractAuthProviderRegistrationUserService,
        generate_otp_code_service: AbstractGenerateOtpCodeService,
        send_mail_service: AbstractSendMailService,
        email_login: str,
    ):
        self.auth_service = auth_service
        self.create_token_service = create_token_service
        self.get_remote_token_service = get_remote_token_service
        self.get_user_info_from_remote_service = get_user_info_from_remote_service
        self.get_user_service = get_user_service
        self.registration_user_service = registration_user_service
        self.update_user_info_service = update_user_info_service
        self.auth_provider_registration_user_service = (
            auth_provider_registration_user_service
        )
        self.generate_otp_code_service = generate_otp_code_service
        self.send_mail_service = send_mail_service
        self._email_login = email_login

    async def authentication(self, form_data) -> Token:
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

    async def authentication_with_code(self, code: str, provider: str) -> RemoteToken:
        remote_token = await self.get_remote_token_service.get_token(
            code=code, provider=provider
        )
        if not remote_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Received an unexpected status from Google",
            )
        user_info = await self.get_user_info_from_remote_service.get_user_info(
            remote_token
        )
        current_user_by_email = await self.get_user_service.get_current_user(
            email=user_info.email
        )
        current_user_by_remote_user_id = await self.get_user_service.get_current_user(
            remote_user_id=user_info.remote_user_id
        )

        if (
            current_user_by_email
            and current_user_by_email.is_active
            and not current_user_by_remote_user_id
        ):
            await self.auth_provider_registration_user_service.create_new_auth_provider(
                user=user_info, provider=provider
            )

        if not current_user_by_email:
            confirmation_code = await self.generate_otp_code_service.generate_code()
            with open("src/templates/registration_mail.html", "r") as file:
                registration_mail = file.read()
                email_content = registration_mail.format(
                    confirmation_code=confirmation_code, recipient_email=user_info.email
                )
                await self.send_mail_service.send_mail(
                    sender_email=self._email_login,
                    recipient_email=user_info.email,
                    email=email_content,
                )
            await self.registration_user_service.create_new_user(
                new_user=user_info, confirmation_code=confirmation_code
            )
            await self.auth_provider_registration_user_service.create_new_auth_provider(
                user=user_info, provider=provider
            )
        return remote_token
