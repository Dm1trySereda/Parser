from typing import Annotated

from fastapi import APIRouter, Depends, Request, status, Query
from fastapi.security import HTTPBasicCredentials

from src.config.auth_provider.auth_provider_config import settings_auth
from src.config.send_mail.send_mail_congif import settings_send_mail
from src.enums.role import UserRoleEnum
from src.models.users import User
from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse
from src.services.auth_provider_registration_user_service.repository import (
    RepositoryAuthProviderRegistrationUserService,
)
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.create_token_service.repository import LocalCreateTokenService
from src.services.email_verification_facade import EmailVerificationFacade
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_from_remote_service.google import GetGoogleUserInfoService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_faсade import RegistrationUserFacade
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)
from src.services.send_mail_service.email import SendMailService
from src.services.update_user_info_service.repository import (
    RepositoryUpdateUserInfoService,
)
from src.services.validate_token_service.repository import (
    RepositoryValidateTokenService,
)

user_routes = APIRouter(tags=["Users"])
auth_facade = AuthorizationFacade(
    validate_token_service_service=RepositoryValidateTokenService()
)


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
        ),
        get_user_info_from_remote_service=GetGoogleUserInfoService(),
        get_user_service=RepositoryGetUserService(request.state.db),
        registration_user_service=RepositoryRegistrationUserService(request.state.db),
        auth_provider_registration_user_service=RepositoryAuthProviderRegistrationUserService(
            request.state.db
        ),
        send_mail_service=SendMailService(
            email_login=settings_send_mail.EMAIL_ADDRESS,
            email_password=settings_send_mail.APPLICATION_PASSWORD,
            smtp_host=settings_send_mail.SMTP_HOST,
            smtp_port=settings_send_mail.SMTP_PORT,
            timeout=settings_send_mail.TIMEOUT,
        ),
        update_user_info_service=RepositoryUpdateUserInfoService(request.state.db),
    )
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
        send_mail_service=SendMailService(
            email_login=settings_send_mail.EMAIL_ADDRESS,
            email_password=settings_send_mail.APPLICATION_PASSWORD,
            smtp_host=settings_send_mail.SMTP_HOST,
            smtp_port=settings_send_mail.SMTP_PORT,
            timeout=settings_send_mail.TIMEOUT,
        ),
    )

    return await regis_facade.registration_user(new_user)


@user_routes.post(
    "/confirmation",
    status_code=status.HTTP_200_OK,
    response_description="email confirmed",
)
async def confirmation(
    request: Request,
    confirmation_code: Annotated[int, Query(qe=4)],
    user: User = Depends(auth_facade.verify_user),
):
    confirmation_facade = EmailVerificationFacade(
        update_user_info_service=RepositoryUpdateUserInfoService(request.state.db)
    )
    await confirmation_facade.verify_email(confirmation_code, user)
    return {"success": f"Email {user.email} confirmed"}


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
