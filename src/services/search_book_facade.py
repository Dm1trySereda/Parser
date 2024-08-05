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
        authors: list = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
        years: list = None,
    ) -> list[BookOuts]:
        if not any(
            [
                book_id,
                book_num,
                title,
                authors,
                price_new,
                price_old,
                rating,
                discount,
                image,
                years,
            ]
        ):
            raise ProvidingParametersError
        book_search_result = await self.search_book_service.search(
            book_id,
            book_num,
            title,
            authors,
            price_new,
            price_old,
            discount,
            rating,
            image,
            years,
        )
        if not book_search_result:
            raise ResultError
        return book_search_result

    async def get_most_popular_authors(self, count):
        popular_authors_result = await self.search_book_service.search_popular(count)
        if not popular_authors_result:
            raise ResultError
        return popular_authors_result

    async def get_publishing_year(self, count):
        publishing_year_result = await self.search_book_service.search_publishing_year(
            count
        )
        if not publishing_year_result:
            raise ResultError
        return publishing_year_result
