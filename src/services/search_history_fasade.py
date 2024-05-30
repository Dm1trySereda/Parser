from fastapi import HTTPException, status

from src.response_schemas.history import HistoryOut
from src.services.book_price_alert_services.abc import \
    AbstractBookPriceAlertService
from src.services.search_history_services.abc import \
    AbstractSearchHistoryService


class HistorySearchFacadeServices:
    def __init__(self, search_history_service: AbstractSearchHistoryService,
                 book_price_alert: AbstractBookPriceAlertService):
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
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        history_search = await self.search_history_service.search(
            book_id,
            book_num,
            title,
            author,
        )
        if not history_search:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        if len(history_search) == 1:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="This book has no story"
            )
        return history_search

    async def get_cheap_books(self) -> list[HistoryOut]:
        cheap_books = await self.book_price_alert.get_price()
        return cheap_books
