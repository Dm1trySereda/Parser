from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.books import Paginate
from src.services.paginate_services.abc import AbstractPaginateBookService


class RepositoryPaginateBookService(AbstractPaginateBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.paginate_instance = Paginate(session)

    async def paginate(self, **kwargs) -> Sequence[Book]:
        page = await self.paginate_instance.select_books(**kwargs)
        return page.scalars().all()
