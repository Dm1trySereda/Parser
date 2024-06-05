from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.models.history import History
from src.repository.history import RepetitiveBook
from src.services.book_price_alert_service.abc import AbstractBookPriceAlertService


class RepositoryBookPriceAlertService(AbstractBookPriceAlertService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.paginate_instance = RepetitiveBook(session)

    async def get_price(self) -> Sequence[History]:
        books_on_page = await self.paginate_instance.select_all_history()
        return books_on_page
