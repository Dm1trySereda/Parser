from sqlalchemy.exc import IntegrityError

from src.request_shemas.parser_book import ParserBook
from src.services.add_new_book_service.abc import AbstractAddNewBookService
from src.services.search_book_service.abc import AbstractSearchBookService
from src.services.update_book_service.abc import AbstractUpdateBookService
from src.services.update_history_service.abc import \
    AbstractUpdateHistoryService


class ParserHandler:
    def __init__(
            self,
            search_services: AbstractSearchBookService,
            update_services: AbstractUpdateBookService,
            insert_services: AbstractAddNewBookService,
            update_history_services: AbstractUpdateHistoryService,

    ):
        self.book_searcher = search_services
        self.book_updater = update_services
        self.book_inserter = insert_services
        self.history_updater = update_history_services

    async def process_books(self, book: ParserBook):
        current_books = await self.book_searcher.search(
            book_num=book.book_num
        )
        if not current_books:
            await self.book_inserter.add_new_book(book)
        else:
            current_book = current_books[0]
            if float(current_book.price_new) != float(book.price_new):
                await self.book_updater.update(current_book, book)

    async def process_books_history(self):
        await self.history_updater.update_history()
