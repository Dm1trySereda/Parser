from fastapi import APIRouter, Request, HTTPException, status

from src.config.auth_provider.auth_provider_config import settings_auth
from src.custom_exceptions.exseptions import RemoteTokenError
from src.services.auth_provider_registration_user_service.repository import (
    RepositoryAuthProviderRegistrationUserService,
)
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.create_token_service.create_local_token import LocalCreateTokenService
from src.services.generate_otp_code_service.generate import GenerateOTPCodeService
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_from_remote_service.google import GetGoogleUserInfoService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
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
        generate_otp_code_service=GenerateOTPCodeService(),
    )
    try:
        remote_user_authenticate = await authenticate_facade.authentication_with_code(
            code, "Google"
        )
    except RemoteTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return remote_user_authenticate
