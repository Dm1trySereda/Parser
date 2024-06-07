import urllib.parse

import httpx
from fastapi import status
from src.response_schemas.users import RemoteToken
from src.services.get_remote_token_service.abc import AbstractGetRemoteTokenService


class GetGoogleTokenService(AbstractGetRemoteTokenService):
    def __init__(
            self,
            google_client_id: str,
            google_client_secret: str,
            google_redirect_url: str,
    ):
        self._google_redirect_url = google_redirect_url
        self._google_client_secret = google_client_secret
        self._google_client_id = google_client_id

    async def get_token(self, **creds) -> RemoteToken | None:
        code = creds.get("code")
        provider = creds.get("provider")
        checkout_token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": urllib.parse.unquote(code),
            "client_id": self._google_client_id,
            "client_secret": self._google_client_secret,
            "redirect_uri": self._google_redirect_url,
            "grant_type": "authorization_code",
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(checkout_token_url, data=data)
        if response.status_code == status.HTTP_200_OK:
            access_token = str(response.json().get("access_token"))
            return RemoteToken(access_token=access_token, token_type="Bearer", provider=provider)
        return None
