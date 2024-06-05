import urllib.parse
from typing import Annotated

import httpx
import requests
from fastapi import APIRouter, Depends, HTTPException, Request, status

from src.config.auth.auth_config import settings_auth
from src.request_shemas.users import GoogleUserRequest
from src.response_schemas.users import UserResponse
from src.services.authorization_facade import check_token, verify_user
from src.services.get_user_in_db_service.repository import RepositoryGetUserService
from src.services.registration_user_faсade import RegistrationUserFacade
from src.services.registration_user_service.repository import (
    RepositoryRegistrationUserService,
)

google_routes = APIRouter(tags=["Google Auth"])


@google_routes.get("/login/google")
async def login_google():
    url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings_auth.GOOGLE_CLIENT_ID}&redirect_uri={settings_auth.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    return {"url": url}


@google_routes.get("/auth/google")
async def auth_google(code: str):
    checkout_token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": urllib.parse.unquote(code),
        "client_id": settings_auth.GOOGLE_CLIENT_ID,
        "client_secret": settings_auth.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings_auth.GOOGLE_REDIRECT_URL,
        "grant_type": "authorization_code",
    }

    response = requests.post(checkout_token_url, data=data)
    if response.status_code != status.HTTP_200_OK:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get the access token.",
        )

    tokens_info = response.json()
    access_token = tokens_info.get("access_token")
    refresh_token = tokens_info.get("refresh_token")

    return {"access_token": access_token, "refresh_token": refresh_token}


@google_routes.post("/registration/google", response_model=UserResponse)
async def reg_google(
    access_token: Annotated[str, Depends(check_token)], request: Request
):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://people.googleapis.com/v1/people/me",
            params={"personFields": "names,emailAddresses"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        if response.status_code == status.HTTP_200_OK:
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
                "is_google_user": True,
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
