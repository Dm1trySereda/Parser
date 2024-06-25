from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.models.books import Book
from src.repository.books import Paginate
from src.services.paginate_service.abc import AbstractPaginateBookService


class RepositoryPaginateBookService(AbstractPaginateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = Paginate(session)

    async def paginate(
        self,
        page: int = None,
        books_quantity: int = None,
        sort_by: SortChoices = None,
        order_asc: bool = None,
    ) -> Sequence[Book]:
        books_on_page = await self.repository.select_books(
            page, books_quantity, sort_by, order_asc
        )
        return books_on_page.scalars().all()
