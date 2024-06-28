from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.books import DeleteBook
from src.response_schemas.books import BookOuts
from src.services.delete_book_service.abc import AbstractDeleteBookService


class RepositoryDeleteBookService(AbstractDeleteBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = DeleteBook(session)

    async def delete_book(
        self, existing_book: BookOuts, book_id: int = None, book_num: int = None
    ) -> BookOuts:
        deleted_book = await self.repository.delete_book(
            existing_book=existing_book, book_id=book_id, book_num=book_num
        )
        return TypeAdapter(BookOuts).validate_python(deleted_book)
