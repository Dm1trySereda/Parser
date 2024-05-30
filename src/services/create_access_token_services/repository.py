from datetime import datetime, timedelta, timezone

import jwt

from src.config.auth.auth_config import settings_auth
from src.services.create_access_token_services.abc import AbstractCreateTokenService


class RepositoryCreateTokenService(AbstractCreateTokenService):
    def __init__(self, data: dict, expires_delta: timedelta | None = None):
        self.data = data
        self.expires_delta = expires_delta

    async def create_access_token(self):
        to_encode = self.data.copy()
        if self.expires_delta:
            expire = datetime.now(timezone.utc) + self.expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(
                minutes=settings_auth.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(
            to_encode, settings_auth.SIGNATURE, algorithm=settings_auth.ALGORITHM
        )
        return encode_jwt
