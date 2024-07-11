from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.security import HTTPBasicCredentials
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.config.auth_provider.auth_provider_config import settings_auth
from src.config.send_mail.send_mail_congif import settings_send_mail
from src.custom_exceptions.exseptions import (
    EmailError,
    OTPCodeError,
    RemoteTokenError,
    UnauthorizedError,
    UsernameError,
)
from src.enums.role import UserRoleEnum
from src.models.users import User
from src.request_shemas.users import UserRequest
from src.response_schemas.users import UserResponse, UserVerifyEmail
from src.services.auth_provider_registration_user_service.repository import (
    RepositoryAuthProviderRegistrationUserService,
)
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_facade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.create_token_service.create_local_token import LocalCreateTokenService
from src.services.email_verification_facade import EmailVerificationFacade
from src.services.generate_otp_code_service.generate import GenerateOTPCodeService
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_from_remote_service.google import GetGoogleUserInfoService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_facade import RegistrationUserFacade
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)
from src.services.render_template_service.render import RenderTemplateService
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


@user_routes.post("/users/signin")
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
        generate_otp_code_service=GenerateOTPCodeService(),
    )
    try:
        user_authentication = await authenticate_facade.authentication(form_data)
    except UnauthorizedError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except RemoteTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return user_authentication


@user_routes.post(
    "/users/signup",
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
        email_login=settings_send_mail.EMAIL_ADDRESS,
        generate_otp_code_service=GenerateOTPCodeService(),
        render_template_service=RenderTemplateService(
            env=Environment(
                loader=FileSystemLoader("src/templates/"),
                autoescape=select_autoescape(["html"]),
            )
        ),
    )
    try:

        user_registration = await regis_facade.registration_user(new_user)
    except UsernameError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )
    except EmailError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    return user_registration


@user_routes.post(
    "/users/verify-email",
    status_code=status.HTTP_200_OK,
    response_model=UserResponse,
    response_description="email confirmed",
)
async def confirmation(
    request: Request,
    confirmation_code: Annotated[int, Query(qe=4)],
    user: User = Depends(auth_facade.verify_user),
):
    confirmation_facade = EmailVerificationFacade(
        update_user_info_service=RepositoryUpdateUserInfoService(request.state.db),
        generate_otp_code_service=GenerateOTPCodeService(),
    )
    try:
        await confirmation_facade.verify_email(
            user_confirmation_code=confirmation_code, recipient_email=user.email
        )
    except OTPCodeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


@user_routes.get(
    "/users/my-profile", status_code=status.HTTP_200_OK, response_model=UserResponse
)
async def about_me(
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin, UserRoleEnum.client]
        )
    )
):
    return user
