from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True
        from_attributes = True


class BookOuts(BaseResponseModel):
    id: Annotated[int, Field(qe=1)]
    book_num: Annotated[int, Field(ge=1, example=123)]
    title: Annotated[str, Field(min_length=1, example="Something title")]
    author: Annotated[str, Field(min_length=1, example="Something author")]
    year: Annotated[int, Field(ge=1900, example=2024)]
    price_new: Annotated[float, Field(ge=0, example=19.99)]
    price_old: Annotated[float | None, Field(ge=0, example=19.99)]
    discount: Annotated[str | None, Field(example="10%")] = None
    rating: Annotated[float | None, Field(ge=0, le=5, example=4.5)] = None
    image: Annotated[str | None, Field(example="https://example.com/image.png")] = None
    created_at: Annotated[datetime, Field(example="2024-05-20T10:00:03")]
    updated_at: Annotated[datetime, Field(example="2024-05-20T10:00:03")]


class PopularAuthor(BaseResponseModel):
    author: Annotated[str, Field()]
    count: Annotated[int, Field()]


class PublishingYear(BaseResponseModel):
    year: Annotated[int, Field()]
    count: Annotated[int, Field()]
