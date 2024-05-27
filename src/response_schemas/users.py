import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class UserResponse(BaseResponseModel):
    username: Annotated[str, Field(min_length=2)]
    email: Annotated[EmailStr | None, Field(min_length=5)] = None
    full_name: Annotated[str | None, Field(min_length=2)] = None
    is_active: Annotated[bool | None, Field()] = None


class UserInDBResponse(UserResponse):
    hashed_password: Annotated[str, Field()]


class Token(BaseResponseModel):
    access_token: Annotated[str, Field()]
    token_type: Annotated[str, Field()]


class TokenData(BaseResponseModel):
    username: Annotated[str | None, Field(min_length=2)] = None
