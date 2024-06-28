from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.books import UpdateBook
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.services.update_book_service.abc import AbstractUpdateBookService


class RepositoryUpdateBookService(AbstractUpdateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = UpdateBook(session)

    async def update(self, existing_book: BookOuts, current_book: BookIn) -> BookOuts:
        updated_book = await self.repository.update_book(
            existing_book=existing_book,
            current_book=current_book.model_dump(by_alias=False),
        )
        return TypeAdapter(BookOuts).validate_python(updated_book)
