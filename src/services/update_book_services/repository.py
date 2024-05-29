from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.books import UpdateBook
from src.request_shemas.books import BookIn
from src.services.update_book_services.abc import AbstractUpdateBookService


class RepositoryUpdateBookService(AbstractUpdateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.book_updater = UpdateBook(session)

    async def update(self, current_book, book: BookIn | dict) -> Book | None:
        # if isinstance(book, dict):
        #     return await self.book_updater.update_book(
        #         current_book=current_book, book=book
        #     )
        # else:
        updated_book = await self.book_updater.update_book(
            current_book=current_book, book=book.dict(by_alias=False)
        )
        await self.session.refresh(updated_book)
        return updated_book
