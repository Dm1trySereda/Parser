from fastapi import HTTPException, status

from src.services.paginate_services.abc import AbstractPaginateBookService


class PaginationFacade:
    def __init__(self, pagination_services: AbstractPaginateBookService):
        self.pagination_services = pagination_services

    async def paginate(self, **kwargs):
        if not any(kwargs.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        page = await self.pagination_services.paginate(**kwargs)
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        return page
