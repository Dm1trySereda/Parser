from fastapi import APIRouter, Request

from src.config.auth.auth_config import settings_auth
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.create_token_service.repository import LocalCreateTokenService
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_from_remote_service.google import GetGoogleUserInfoService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)
from src.services.validate_token_service.repository import RepositoryValidateTokenService

google_routes = APIRouter(tags=["Google Auth"])


@google_routes.get("/login/google")
async def login_google():
    url_redirect = (
        f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings_auth.GOOGLE_CLIENT_ID}"
        f"&redirect_uri={settings_auth.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline")
    return {"url": url_redirect}


@google_routes.get("/auth/google")
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
    )
    return await authenticate_facade.authentication_with_code(code, "Google")


authorization_facade = AuthorizationFacade(
    validate_token_service_service=RepositoryValidateTokenService()
)
