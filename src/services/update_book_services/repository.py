from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import UpdateBook
from src.request_shemas.books import BookIn
from src.services.update_book_services.abc import AbstractUpdateBookService


class RepositoryUpdateBookService(AbstractUpdateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update(self, book: BookIn) -> Book | None:
        book_updater = UpdateBook(self.session)
        return await book_updater.update_book(book.model_dump(by_alias=False))
