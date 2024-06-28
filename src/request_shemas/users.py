import re
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic.alias_generators import to_camel


class BaseRequestModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class UserRequest(BaseRequestModel):
    username: Annotated[str, Field(min_length=2)]
    password: Annotated[str, Field(min_length=2)]
    full_name: Annotated[str | None, Field(min_length=2)] = None
    email: Annotated[EmailStr | None, Field(min_length=5)] = None

    @field_validator("username")
    @classmethod
    def no_special_symbols_username(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-Я0-9_-]*$", value):
            raise ValueError("Field cannot contain special symbols")
        return value

    @field_validator("full_name")
    @classmethod
    def no_special_symbols_full_name(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-Я\s-]*$", value):
            raise ValueError("Field cannot contain special symbols")
        return value
