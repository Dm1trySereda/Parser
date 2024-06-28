from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UserResponse(BaseResponseModel):
    id: Annotated[int | None, Field(qe=1)] = None
    username: Annotated[str | None, Field(min_length=2)] = None
    full_name: Annotated[str | None, Field(min_length=2)] = None
    email: Annotated[EmailStr | None, Field(min_length=5)] = None
    hashed_password: Annotated[str | None, Field()] = None
    created_at: Annotated[datetime | None, Field(example="2024-05-20T10:00:03")] = None
    updated_at: Annotated[datetime | None, Field(example="2024-05-20T10:00:03")] = None
    is_active: Annotated[bool, Field()] = None
    role_id: Annotated[int | None, Field()] = None


class RemoteUserInfoResponse(BaseResponseModel):
    remote_user_id: Annotated[int, Field(qe=1)]
    full_name: Annotated[str | None, Field(min_length=2)] = None
    email: Annotated[EmailStr | None, Field(min_length=5)] = None


class UserVerifyEmail(BaseResponseModel):
    username: Annotated[str | None, Field(min_length=2)]
    email: Annotated[EmailStr | None, Field(min_length=5)]
    is_active: Annotated[bool, Field()]


class Token(BaseResponseModel):
    access_token: Annotated[str, Field()]
    token_type: Annotated[str, Field()]


class RemoteToken(Token):
    provider: str


class OneTimePassword(BaseResponseModel):
    user_email: Annotated[EmailStr | None, Field()]
    user_secret: Annotated[str, Field()]
    qrcode: Annotated[str, Field()]
    otp_code: Annotated[int, Field()]
