import urllib.parse
from datetime import datetime, timedelta, timezone

import httpx
import jwt

from src.config.auth.auth_config import settings_auth
from src.response_schemas.users import Token
from src.services.create_token_service.abc import AbstractCreateTokenService


class LocalCreateTokenService(AbstractCreateTokenService):

    async def create_access_token(
            self, data: dict, expires_delta: timedelta | None = None
    ) -> Token:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings_auth.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, settings_auth.SIGNATURE, algorithm=settings_auth.ALGORITHM
        )
        return encode_jwt
