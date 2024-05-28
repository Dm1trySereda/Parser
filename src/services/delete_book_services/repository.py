from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.books import DeleteBook
from src.services.delete_book_services.abc import AbstractDeleteBookService


class RepositoryDeleteBookService(AbstractDeleteBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.deleter = DeleteBook(session)

    async def delete_book(self, current_book, **kwargs) -> Book | None:
        return await self.deleter.delete_book(current_book, **kwargs)
