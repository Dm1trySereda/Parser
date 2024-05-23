from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import Paginate
from src.services.paginate_book_services.abc import AbstractPaginateBookService


class RepositoryPaginateBookService(AbstractPaginateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def paginate(self, **kwargs) -> Sequence[Book]:
        paginate_page = Paginate(self.session)
        return await paginate_page.select_books(**kwargs)
