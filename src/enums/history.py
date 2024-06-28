from enum import Enum


class HistorySortChoices(Enum):
    id = "book_id"
    book_num = "book_num"
    title = "title"
    price = "price"
    created_at = "created_at"
    updated_at = "updated_at"
