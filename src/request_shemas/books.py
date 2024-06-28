import re
from typing import Annotated

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic.alias_generators import to_camel


class BaseRequestModel(BaseModel):
    class Config:
        alias_generator = to_camel


class BookIn(BaseRequestModel):
    book_num: Annotated[int, Field(ge=1, example=123)]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    author: Annotated[str, Field(min_length=2, example="Something author")]
    price_new: Annotated[float, Field(ge=0, example=19.99)]
    price_old: Annotated[float | None, Field(ge=0, example=17.99)] = None
    discount: Annotated[
        str | None, Field(min_length=2, max_length=4, example="10%")
    ] = None
    rating: Annotated[float | None, Field(ge=0, le=5, example=4.5)] = None
    image_url: Annotated[HttpUrl, Field()] = None

    @field_validator("title", "author")
    @classmethod
    def validate(cls, value):

        if not re.match(r"^[a-zA-Zа-яА-Я0-9\s(),'\"]*$", value):
            raise ValueError("The field cannot contain special symbols.")

        new_value = " ".join(value.split())
        if new_value != value:
            raise ValueError("The field contains extra spaces.")

        return new_value


class ParserBook(BookIn):
    class Config:
        alias_generator = False
        populate_by_name = True
