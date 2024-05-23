from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import DeleteBook
from src.services.delete_book_services.abc import AbstractDeleteBookService


class RepositoryDeleteBookService(AbstractDeleteBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def delete_book(self, **kwargs) -> Book | None:
        inserter = DeleteBook(self.session)
        return await inserter.delete_book(**kwargs)
