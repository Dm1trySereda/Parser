from sqlalchemy.ext.asyncio import AsyncSession
from src.models.history import History
from src.repository.history import RepetitiveBook
from src.services.book_price_alert_service.abc import AbstractBookPriceAlertService


class RepositoryBookPriceAlertService(AbstractBookPriceAlertService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = RepetitiveBook(session)

    async def get_price(self) -> list[History]:
        books_on_page = await self.repository.select_all_history()
        return books_on_page
