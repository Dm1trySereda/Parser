from datetime import datetime
from typing import Annotated

from pydantic import BaseModel, Field


class HistoryOut(BaseModel):
    book_num: Annotated[int, Field(ge=1, example=123, serialization_alias="bookNum")]
    created_at: Annotated[
        datetime, Field(example="2024-05-20T10:00:03", serialization_alias="createdAt")
    ]
    updated_at: Annotated[
        datetime, Field(example="2024-05-20T10:00:03", serialization_alias="updatedAt")
    ]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    price: Annotated[float, Field(ge=0, example=19.99, serialization_alias="priceNew")]
    image: Annotated[str | None, Field(example="https://example.com/image.png")] = None

    class Config:
        allow_population_by_field_name = True
        from_attributes = True
        orm_mode = True
