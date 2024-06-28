from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.repositories.books import Paginate
from src.response_schemas.books import BookOuts
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
    ) -> list[BookOuts]:
        books_on_page = await self.repository.select_books(
            page, books_quantity, sort_by, order_asc
        )
        return TypeAdapter(list[BookOuts]).validate_python(
            books_on_page.scalars().all()
        )
