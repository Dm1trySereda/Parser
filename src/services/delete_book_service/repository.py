from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repositories.books import DeleteBook
from src.services.delete_book_service.abc import AbstractDeleteBookService


class RepositoryDeleteBookService(AbstractDeleteBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.deleter = DeleteBook(session)

    async def delete_book(
        self, current_book, book_id: int = None, book_num: int = None
    ) -> Book:
        return await self.deleter.delete_book(
            current_book=current_book, book_id=book_id, book_num=book_num
        )
