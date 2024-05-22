from enum import Enum


class SortChoices(Enum):
    id = "id"
    book_num = "book_num"
    title = "title"
    author = "author"
    price_new = "price_new"
    price_old = "price_old"
    discount = "discount"
    rating = "rating"
    created_at = "created_at"
    updated_at = "updated_at"
