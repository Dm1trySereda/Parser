from src.custom_exceptions.exseptions import DuplicateError
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.services.create_new_book_service.abc import AbstractAddNewBookService
from src.services.search_book_service.abc import AbstractSearchBookService
from src.services.update_history_service.abc import AbstractUpdateHistoryService


class AddNewBookFacade:
    def __init__(
        self,
        search_services: AbstractSearchBookService,
        inserter_services: AbstractAddNewBookService,
        history_updater_services: AbstractUpdateHistoryService,
    ):
        self.search_services = search_services
        self.inserter_services = inserter_services
        self.history_updater_services = history_updater_services

    async def add_new_book(self, new_book: BookIn) -> BookOuts:
        current_books = await self.search_services.search(book_num=new_book.book_num)
        if not current_books:
            new_book_record = await self.inserter_services.add_new_book(new_book)
            await self.history_updater_services.update_history()
        else:
            raise DuplicateError
        return new_book_record
