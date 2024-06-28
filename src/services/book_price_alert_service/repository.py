from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.history import HistorySortChoices
from src.repositories.history import RepetitiveBook
from src.response_schemas.history import HistoryOut
from src.services.book_price_alert_service.abc import AbstractBookPriceAlertService
from pydantic import TypeAdapter


class RepositoryBookPriceAlertService(AbstractBookPriceAlertService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = RepetitiveBook(session)

    async def get_price(
        self,
        page: int,
        books_quantity: int,
        sort_by: HistorySortChoices,
        order_asc: bool,
    ) -> list[HistoryOut]:
        books_on_page = await self.repository.select_all_history(
            page,
            books_quantity,
            sort_by,
            order_asc,
        )
        return TypeAdapter(list[HistoryOut]).validate_python(books_on_page)
