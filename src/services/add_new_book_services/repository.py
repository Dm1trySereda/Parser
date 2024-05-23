from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import InsertBook
from src.request_shemas.books import BookIn
from src.services.add_new_book_services.abc import AbstractAddNewBookService


class RepositoryAddNewBookService(AbstractAddNewBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_new_book(self, new_book: BookIn) -> Book | None:
        inserter = InsertBook(self.session)
        return await inserter.insert_new_book(new_book.model_dump(by_alias=False))

