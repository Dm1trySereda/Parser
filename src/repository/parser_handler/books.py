from src.config.database.db_helpers import db_helper
from src.repository.parser_handler.history import HistoryRepository
from src.services.parser_services.repository import RepositoryParserBookService, AbstractParserBookService


class BaseHandler:
    def __init__(self):
        self.get_async_session = db_helper.get_db_session()

    async def process_books(self, pages: list) -> None:
        async with self.get_async_session as async_session:
            book_handler: AbstractParserBookService = RepositoryParserBookService(async_session)
            book_updater: AbstractParserBookService = RepositoryParserBookService(async_session)
            for books in pages:
                for book in books:
                    new_book = await book_handler.add_new_book(book)
                    await book_updater.update_book(book) if new_book is None else new_book
            await async_session.commit()

    async def process_books_history(self):
        async with self.get_async_session as async_session:
            history_handler = HistoryRepository(async_session)
            await history_handler.update_books_history()
