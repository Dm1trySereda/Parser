from fastapi import APIRouter, Request

from src.config.auth_provider.auth_provider_config import settings_auth
from src.config.send_mail.send_mail_congif import settings_send_mail
from src.services.auth_provider_registration_user_service.repository import (
    RepositoryAuthProviderRegistrationUserService,
)
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.create_token_service.repository import LocalCreateTokenService
from src.services.generate_otp_code_service.generate import GenerateOtpCodeService
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_from_remote_service.google import GetGoogleUserInfoService
from src.services.get_user_service.repository import RepositoryGetUserService
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

google_routes = APIRouter(tags=["Google Auth"])


@google_routes.get("/start-google-login")
async def login_google():
    url_redirect = (
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings_auth.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings_auth.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    )
    return {"url": url_redirect}


@google_routes.get("/process-google-login")
async def auth_google(code: str, request: Request):
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
        email_login=settings_send_mail.EMAIL_ADDRESS,
        generate_otp_code_service=GenerateOtpCodeService(),
        update_user_info_service=RepositoryUpdateUserInfoService(request.state.db),
    )
    return await authenticate_facade.authentication_with_code(code, "Google")


authorization_facade = AuthorizationFacade(
    validate_token_service_service=RepositoryValidateTokenService()
)
