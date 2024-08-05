from src.custom_exceptions.exseptions import ProvidingParametersError, ResultError
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
        authors: list = None,
        years: list = None,
    ) -> list[BookOuts]:
        page = await self.pagination_services.paginate(
            page, books_quantity, sort_by, order_asc, authors, years
        )
        if not page:
            raise ResultError
        return page
