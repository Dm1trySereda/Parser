from src.request_shemas.books import BookIn


class ParserBook(BookIn):
    class Config:
        alias_generator = False
        populate_by_name = True
