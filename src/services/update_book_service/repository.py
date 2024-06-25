from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.books import UpdateBook
from src.request_shemas.books import BookIn
from src.services.update_book_service.abc import AbstractUpdateBookService


class RepositoryUpdateBookService(AbstractUpdateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UpdateBook(session)

    async def update(self, existing_book: Book, current_book: BookIn) -> Book:
        updated_book = await self.repository.update_book(
            existing_book=existing_book,
            current_book=current_book.model_dump(by_alias=False),
        )
        await self.session.refresh(updated_book)
        return updated_book
