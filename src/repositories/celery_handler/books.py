from src.config.database.db_helpers import db_helper
from src.repositories.api_action.books import InsertBook, UpdateBook
from src.repositories.celery_handler.history import HistoryRepository


class BaseHandler:
    def __init__(self):
        self.get_async_session = db_helper.get_db_session()

    async def process_books(self, pages: list) -> None:
        async with self.get_async_session as async_session:
            book_handler = InsertBook(async_session)
            book_updater = UpdateBook(async_session)
            for books in pages:
                for book in books:
                    existing_book = await book_handler.select_book(book_num=book["book_num"])
                    if existing_book is not None:
                        await book_updater.update_book(book)
                    else:
                        await book_handler.insert_new_book(book)

            await async_session.commit()

    async def process_books_history(self):
        async with self.get_async_session as async_session:
            history_handler = HistoryRepository(async_session)
            await history_handler.update_books_history()
