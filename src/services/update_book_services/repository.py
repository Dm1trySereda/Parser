from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import UpdateBook
from src.request_shemas.books import BookIn
from src.services.update_book_services.abc import AbstractUpdateBookService
from src.services.search_book_services.repository import RepositorySearchBookService


class RepositoryUpdateBookService(AbstractUpdateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_service = RepositorySearchBookService(session)

    async def update(self, book: BookIn) -> Book | None:
        current_book = await self.search_service.search(book_num=book.book_num)
        if current_book:
            book_updater = UpdateBook(self.session)
            updated_book = await book_updater.update_book(current_book=current_book,
                                                          book=book.dict(by_alias=False))
            await self.session.refresh(updated_book)
            return updated_book
        return current_book
