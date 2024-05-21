from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        from_attributes = True
        orm_mode = True


class BookIn(BaseResponseModel):
    book_num: Annotated[int, Field(ge=1, example=123)]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    author: Annotated[str, Field(min_length=2, example="Something author")]
    price_new: Annotated[float, Field(ge=0, example=19.99)]
    rating: Annotated[float | None, Field(ge=0, le=5, example=4.5)] = None
    image: Annotated[str | None, Field(example="https://example.com/image.png")] = None


class BookOuts(BookIn):
    book_num: Annotated[int, Field(ge=1, example=123, serialization_alias="bookNum")]
    created_at: Annotated[
        datetime, Field(example="2024-05-20T10:00:03", serialization_alias="createdAt")
    ]
    updated_at: Annotated[
        datetime, Field(example="2024-05-20T10:00:03", serialization_alias="updatedAt")
    ]
    price_old: Annotated[float | None, Field(ge=0, example=19.99)]
    discount: Annotated[str | None, Field(example="10%")] = None

    class Config:
        alias_generator = False
