from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import DeleteBook, BaseRepository
from src.services.delete_book_services.abc import AbstractDeleteBookService
from src.services.search_book_services.repository import RepositorySearchBookService


class RepositoryDeleteBookService(AbstractDeleteBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_service = RepositorySearchBookService(session)

    async def delete_book(self, **kwargs) -> Book | None:
        existing_book = BaseRepository(self.session)
        current_book = await self.search_service.search(book_num=kwargs.get("book_num"))
        if current_book:
            inserter = DeleteBook(self.session)
            return await inserter.delete_book(current_book, **kwargs)
        return None
