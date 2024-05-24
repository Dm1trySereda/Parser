from typing import Tuple

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import InsertBook, UpdateBook, DeleteDuplicateBooks
from src.services.parser_services.abc import AbstractParserBookService
from src.services.search_book_services.repository import RepositorySearchBookService


class RepositoryParserBookService(AbstractParserBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_service = RepositorySearchBookService(session)

    async def delete_duplicate(self):
        deleter_duplicate = DeleteDuplicateBooks(self.session)
        return await deleter_duplicate.remove_duplicates()

    async def check_book(self, **kwargs: dict) -> Book | None:
        return await self.search_service.search(book_num=kwargs.get("book_num"))

    async def add_new_book(self, new_book: dict) -> Book | None:
        inserter = InsertBook(self.session)
        return await inserter.insert_new_book(new_book)

    async def update_book(self, current_book, book: dict) -> Book | None:
        updater = UpdateBook(self.session)
        return await updater.update_book(current_book, book)
