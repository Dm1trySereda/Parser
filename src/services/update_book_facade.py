from src.custom_exceptions.exseptions import ResultError
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.services.search_book_service.abc import AbstractSearchBookService
from src.services.update_book_service.abc import AbstractUpdateBookService
from src.services.update_history_service.abc import AbstractUpdateHistoryService


class UpdateBookFacade:
    def __init__(
        self,
        searcher_services: AbstractSearchBookService,
        updater_services: AbstractUpdateBookService,
        history_updater_services: AbstractUpdateHistoryService,
    ):
        self.searcher = searcher_services
        self.updater = updater_services
        self.history_inserter = history_updater_services

    async def update_book(self, current_book: BookIn) -> BookOuts:
        existing_book = await self.searcher.search(book_num=current_book.book_num)
        if existing_book:
            update_book = await self.updater.update(
                existing_book=existing_book[0], current_book=current_book
            )
            await self.history_inserter.update_history()
        else:
            raise ResultError
        return update_book
