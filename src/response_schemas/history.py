from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class HistoryOut(BaseModel):
    book_num: Annotated[int, Field(ge=1, example=123, serialization_alias="bookNum")]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    price: Annotated[float, Field(ge=0, example=19.99)]
    updated_at: Annotated[
        datetime, Field(example="2024-05-20T10:00:03", serialization_alias="updatedAt")
    ]

    class Config:
        populate_by_name = True
        from_attributes = True
