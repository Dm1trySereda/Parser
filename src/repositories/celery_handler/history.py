from sqlalchemy import exists, insert, select


from src.models.books import Book
from src.models.history import History
from src.repositories.api_action.books import BaseRepository


class HistoryRepository(BaseRepository):
    async def update_books_history(self):
        stmt = insert(History).from_select(
            ["book_id", "created_at", "updated_at", "book_num", "title", "price"],
            select(
                Book.id,
                Book.created_at,
                Book.updated_at,
                Book.book_num,
                Book.title,
                Book.price_new,
            ).where(
                ~exists()
                .where(History.book_num == Book.book_num)
                .where(History.price == Book.price_new)
            ),
        )

        await self.async_session.execute(stmt)
        await self.async_session.commit()
