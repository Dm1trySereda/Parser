from src.custom_exceptions.exseptions import ProvidingParametersError, ResultError
from src.response_schemas.books import BookOuts
from src.services.search_book_service.abc import AbstractSearchBookService


class BookSearchFacadeServices:
    def __init__(self, search_book_service: AbstractSearchBookService):
        self.search_book_service = search_book_service

    async def search_book(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
    ) -> list[BookOuts]:
        if not any(
            [
                book_id,
                book_num,
                title,
                author,
                price_new,
                price_old,
                rating,
                discount,
                image,
            ]
        ):
            raise ProvidingParametersError
        book_search_result = await self.search_book_service.search(
            book_id,
            book_num,
            title,
            author,
            price_new,
            price_old,
            discount,
            rating,
            image,
        )
        if not book_search_result:
            raise ResultError
        return book_search_result
