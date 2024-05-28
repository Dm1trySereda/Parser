from src.repository.history import UpdateHistory
from src.request_shemas.books import BookIn
from src.services.search_book_services.repository import RepositorySearchBookService, AbstractSearchBookService
from src.services.add_new_book_services.repository import RepositoryAddNewBookService, AbstractAddNewBookService
from src.services.update_book_services.repository import RepositoryUpdateBookService, AbstractUpdateBookService
from src.config.database.db_helpers import db_helper
from sqlalchemy.exc import IntegrityError


class ParserHandler:
    def __init__(self):
        self.async_session = db_helper.get_db_session()

    async def process_books(self, pages: list):
        if not pages:
            raise ValueError("Page not found")
        async with self.async_session as session:
            book_searcher: AbstractSearchBookService = RepositorySearchBookService(session)
            book_updater: AbstractUpdateBookService = RepositoryUpdateBookService(session)
            book_inserter: AbstractAddNewBookService = RepositoryAddNewBookService(session)
            for books in pages:
                for book in books:
                    try:
                        current_books = await book_searcher.search(
                            book_num=book.get("book_num")
                        )
                        if not current_books:
                            await book_inserter.add_new_book(book)
                        else:
                            current_book = current_books[0]
                            if float(current_book.price_new) != float(book.get("price_new")):
                                await book_updater.update(current_book, book)
                        await session.commit()
                    except IntegrityError:
                        await session.rollback()

    async def process_books_history(self):
        async with self.async_session as session:
            history_updater = UpdateHistory(session)
            await history_updater.update_books_history()

#
# class DeleteDuplicateHandler(BaseHandler):
#     async def remove_duplicates(self):
#         async with self.get_async_session as async_session:
#             book_handler: AbstractParserBookService = RepositoryParserBookService(
#                 async_session
#             )
#             await book_handler.delete_duplicate()
#             await async_session.commit()
