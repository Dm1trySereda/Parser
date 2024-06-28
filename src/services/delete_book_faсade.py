from src.custom_exceptions.exseptions import ProvidingParametersError, ResultError
from src.response_schemas.books import BookOuts
from src.services.delete_book_service.abc import AbstractDeleteBookService
from src.services.search_book_service.abc import AbstractSearchBookService


class DeleteBookFacade:
    def __init__(
        self,
        search_services: AbstractSearchBookService,
        delete_services: AbstractDeleteBookService,
    ):
        self.book_searcher = search_services
        self.book_deleter = delete_services

    async def delete_book(self, book_id: int = None, book_num: int = None) -> BookOuts:
        if not any([book_id, book_num]):
            raise ProvidingParametersError
        existing_book = await self.book_searcher.search(book_id, book_num)
        if existing_book:
            delete_book = await self.book_deleter.delete_book(
                existing_book=existing_book[0], book_id=book_id, book_num=book_num
            )
        else:
            raise ResultError
        return delete_book
