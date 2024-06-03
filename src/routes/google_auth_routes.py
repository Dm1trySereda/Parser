import urllib.parse
from typing import Annotated

import requests
from fastapi import APIRouter, HTTPException, status, Depends

from src.response_schemas.users import UserResponse
from src.services.authorization_facade import verify_user
from src.config.auth.auth_config import settings_auth

google_routes = APIRouter(tags=["Google Auth"])


@google_routes.get("/login/google")
async def login_google():
    url = f"https://accounts.google.com/o/oauth2/auth?response_type=code&client_id={settings_auth.GOOGLE_CLIENT_ID}&redirect_uri={settings_auth.GOOGLE_REDIRECT_URL}&scope=openid%20profile%20email&access_type=offline"
    return {"url": url}


@google_routes.get("/auth/google")
async def auth_google(code: str):
    TOKEN_URL = "https://oauth2.googleapis.com/token"
    data = {
        "code": urllib.parse.unquote(code),
        "client_id": settings_auth.GOOGLE_CLIENT_ID,
        "client_secret": settings_auth.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings_auth.GOOGLE_REDIRECT_URL,
        "grant_type": "authorization_code",
    }

    response = requests.post(TOKEN_URL, data=data)
    if response.status_code != 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to get the access token.",
        )

    tokens_info = response.json()
    access_token = tokens_info.get("access_token")
    refresh_token = tokens_info.get("refresh_token")

    return {"access_token": access_token, "refresh_token": refresh_token}


@google_routes.get("/google/about/me")
async def about(access_token: Annotated[UserResponse, Depends(verify_user)]):
    response = requests.get(
        'https://people.googleapis.com/v1/people/me',
        params={'personFields': 'emailAddresses,names,photos'},
        headers={'Authorization': f'Bearer {access_token}'},
    )

    profile_info = response.json()
    return profile_info
