from src.custom_exceptions.exseptions import (
    ResultError,
    BookHistoryError,
    ProvidingParametersError,
)
from src.enums.history import HistorySortChoices
from src.response_schemas.history import HistoryOut
from src.services.book_price_alert_service.abc import AbstractBookPriceAlertService
from src.services.search_history_service.abc import AbstractSearchHistoryService


class HistorySearchFacadeServices:
    def __init__(
        self,
        search_history_service: AbstractSearchHistoryService,
        book_price_alert: AbstractBookPriceAlertService,
    ):
        self.search_history_service = search_history_service
        self.book_price_alert = book_price_alert

    async def search_history(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
    ) -> list[HistoryOut]:
        if not any(
            [
                book_id,
                book_num,
                title,
                author,
            ]
        ):
            raise ProvidingParametersError
        history_search = await self.search_history_service.search(
            book_id,
            book_num,
            title,
            author,
        )
        if not history_search or len(history_search) == 1:
            raise BookHistoryError
        return history_search

    async def get_cheap_books(
        self,
        page: int = 1,
        books_quantity: int = 10,
        sort_by: HistorySortChoices = HistorySortChoices.price,
        order_asc: bool = True,
    ) -> list[HistoryOut]:
        cheap_books = await self.book_price_alert.get_price(
            page, books_quantity, sort_by, order_asc
        )
        if not cheap_books:
            raise ResultError
        return cheap_books
