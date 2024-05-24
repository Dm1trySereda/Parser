from src.config.database.db_helpers import db_helper
from src.models import Book
from src.repository.parser_handler.history import HistoryRepository
from src.services.parser_services.repository import (
    RepositoryParserBookService,
    AbstractParserBookService,
)


class BaseHandler:
    def __init__(self):
        self.get_async_session = db_helper.get_db_session()

    async def process_books(self, pages: list):
        async with self.get_async_session as async_session:
            book_handler: AbstractParserBookService = RepositoryParserBookService(
                async_session
            )
            for books in pages:
                for book in books:
                    current_book = await book_handler.check_book(
                        book_num=book.get("book_num")
                    )
                    if current_book is None:
                        await book_handler.add_new_book(book)
                    elif current_book.book_num == book.get(
                        "book_num"
                    ) and current_book.price_new != book.get("price_new"):
                        await book_handler.update_book(
                            current_book=current_book, book=book
                        )
            await async_session.commit()

    async def process_books_history(self):
        async with self.get_async_session as async_session:
            history_handler = HistoryRepository(async_session)
            await history_handler.update_books_history()


class DeleteDuplicateHandler(BaseHandler):
    async def remove_duplicates(self):
        async with self.get_async_session as async_session:
            book_handler: AbstractParserBookService = RepositoryParserBookService(
                async_session
            )
            await book_handler.delete_duplicate()
            await async_session.commit()
