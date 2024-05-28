from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.paginate_services.repository import (
    AbstractPaginateBookService,
    RepositoryPaginateBookService,
)


class PaginationFacade:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.pagination: AbstractPaginateBookService = RepositoryPaginateBookService(
            session
        )

    async def paginate(self, **kwargs):
        if not any(kwargs.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        page = await self.pagination.paginate(**kwargs)
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        return page
