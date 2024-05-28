from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.search_book_services.repository import (
    AbstractSearchBookService,
    RepositorySearchBookService,
)


class BookSearchFacadeServices:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_book_service: AbstractSearchBookService = (
            RepositorySearchBookService(session)
        )

    async def search_book(self, **kwargs):
        if not any(kwargs.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        book_search_result = await self.search_book_service.search(**kwargs)
        if not book_search_result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        return book_search_result
