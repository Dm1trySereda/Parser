from pydantic import BaseModel


class Book(BaseModel):
    book_num: int
    title: str
    author: str
    price: float
    rating: float | None = None
    image: str | None = None
