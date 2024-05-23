import re
from typing import Annotated, Optional

from pydantic import BaseModel, Field, HttpUrl, field_validator
from pydantic.alias_generators import to_camel

forbidden_words = [
    "Говно",
    "залупа",
    "пенис",
    "хер",
    "давалка",
    "хуй",
    "блядина",
    "Головка",
    "шлюха",
    "жопа",
    "член",
    "еблан",
    "петух",
    "Мудила",
    "Рукоблуд",
    "ссанина",
    "очко",
    "блядун",
    "вагина",
    "Сука",
    "ебланище",
    "влагалище",
    "пердун",
    "дрочила",
    "Пидор",
    "пизда",
    "туз",
    "малафья",
    "Гомик",
    "мудила",
    "пилотка",
    "манда",
    "Анус",
    "вагина",
    "путана",
    "педрила",
    "Шалава",
    "хуило",
    "мошонка",
    "елда",
]


class BaseResponseModel(BaseModel):
    class Config:
        alias_generator = to_camel


class BookIn(BaseResponseModel):
    book_num: Annotated[int, Field(ge=1, example=123)]
    title: Annotated[str, Field(min_length=2, example="Something title")]
    author: Annotated[str, Field(min_length=2, example="Something author")]
    price_new: Annotated[float, Field(ge=0, example=19.99)]
    price_old: Annotated[float | None, Field(ge=0)] = None
    discount: Annotated[str | None, Field(min_length=2, max_length=4)] = None
    rating: Optional[float] = Field(None, ge=0, le=5, example=4.5)
    image_url: Optional[HttpUrl] = Field(None)

    @field_validator("title", "author")
    @classmethod
    def no_forbidden_words(cls, value):
        if any(word.lower() in value for word in forbidden_words):
            raise ValueError("Field contains forbidden words")
        return value

    @field_validator("title", "author")
    @classmethod
    def no_special_symbols(cls, value):
        if not re.match(r"^[a-zA-Zа-яА-Я0-9\s()'\"]*$", value):
            raise ValueError("Field cannot contain special symbols")
        return value

    @field_validator("title", "author")
    @classmethod
    def no_extra_spaces(cls, value):
        new_value = " ".join(value.split())
        if new_value != value:
            raise ValueError("Field contains extra spaces")
        return new_value
