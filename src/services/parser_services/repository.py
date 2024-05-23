from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import InsertBook, UpdateBook
from src.services.parser_services.abc import AbstractParserBookService


class RepositoryParserBookService(AbstractParserBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_book(self, new_book: dict) -> Book | None:
        inserter = InsertBook(self.session)
        return await inserter.insert_new_book(new_book)

    async def update_book(self, new_book: dict) -> Book | None:
        inserter = UpdateBook(self.session)
        return await inserter.update_book(new_book)
