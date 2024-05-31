from fastapi import HTTPException, status

from src.enums.book import SortChoices
from src.response_schemas.books import BookOuts
from src.services.paginate_service.abc import AbstractPaginateBookService


class PaginationFacade:
    def __init__(self, pagination_services: AbstractPaginateBookService):
        self.pagination_services = pagination_services

    async def paginate(
        self,
        page: int = None,
        books_quantity: int = None,
        sort_by: SortChoices = None,
        order_asc: bool = None,
    ) -> list[BookOuts]:
        if not any([page, books_quantity, sort_by, order_asc]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        page = await self.pagination_services.paginate(
            page, books_quantity, sort_by, order_asc
        )
        if not page:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
            )
        return page
