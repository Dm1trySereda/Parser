from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True


class HistoryOut(BaseResponseModel):
    book_id: Annotated[int, Field(qe=1)]
    book_num: Annotated[int, Field(ge=1, example=123)]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    price: Annotated[float, Field(ge=0, example=19.99)]
    created_at: Annotated[datetime, Field(example="2024-05-20T10:00:03")]
    updated_at: Annotated[datetime, Field(example="2024-05-20T10:00:03")]
