import urllib.parse
from typing import Annotated

import httpx
import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.config.auth.auth_config import settings_auth
from src.request_shemas.users import GoogleUserRequest
from src.response_schemas.users import UserResponse
from src.services.auth_services.repository import RepositoryAuthUserService
from src.services.authentication_faсade import AuthenticateUserFacade
from src.services.authorization_facade import AuthorizationFacade
from src.services.get_remote_token_service.google import GetGoogleTokenService
from src.services.get_user_service.repository import RepositoryGetUserService
from src.services.registration_user_faсade import RegistrationUserFacade
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)
from src.services.validate_token.repository import RepositoryValidateTokenService
from src.services.create_token_service.repository import LocalCreateTokenService

google_routes = APIRouter(tags=["Google Auth"])


@google_routes.get("/login/google")
async def login_google():
    url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings_auth.GOOGLE_CLIENT_ID}&redirect_uri={settings_auth.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    return {"url": url}


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
    )
    return await authenticate_facade.authentication_with_code(code, "google")


authorization_facade = AuthorizationFacade(
    validate_token_service=RepositoryValidateTokenService()
)


@google_routes.post("/registration/google", response_model=UserResponse)
async def reg_google(
        access_token: Annotated[str, Depends(authorization_facade.verify_user)],
        request: Request,
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://people.googleapis.com/v1/people/me",
            params={"personFields": "names,emailAddresses"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code == status.HTTP_200_OK:
            print("Пользователь получен")
            profile_info = response.json()
            email_data = profile_info["emailAddresses"][0]
            user_id = email_data["metadata"]["source"]["id"]
            email_value = email_data["value"]
            full_name_data = profile_info["names"][0]
            full_name = full_name_data["displayName"]
            user_info = {
                "username": user_id,
                "full_name": full_name,
                "email": email_value,
            }
            regis_facade = RegistrationUserFacade(
                search_services=RepositoryGetUserService(request.state.db),
                registration_services=RepositoryRegistrationUserService(
                    request.state.db
                ),
            )

            return await regis_facade.registration_user(
                new_user=GoogleUserRequest(**user_info)
            )
        else:
            print("hueta")
