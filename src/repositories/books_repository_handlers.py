from sqlalchemy import exists, insert, select

from src.config.database.db_helpers import db_helper
from src.models.books import Book
from src.models.history import History


class BaseHandler:
    def __init__(self):
        self.get_async_session = db_helper.get_db_session()

    async def process_books(self, pages: list) -> None:
        async with self.get_async_session as async_session:
            book_handler = BookHandler(async_session)
            for books in pages:
                for book in books:
                    stmt = select(Book).where(Book.book_num == book["book_num"])
                    result = await async_session.execute(stmt)
                    existing_book = result.scalars().first()
                    if existing_book:
                        await book_handler.update_table_book(book, existing_book)
                    else:
                        await book_handler.add_book(book)

            await async_session.commit()

    async def process_books_history(self):
        async with self.get_async_session as async_session:
            book_history_handler = HistoryHandler(async_session)
            await book_history_handler.update_books_history()


class BookHandler:
    def __init__(self, async_session):
        self.async_session = async_session

    async def add_book(self, book: dict) -> None:
        new_book = Book(
            book_num=book["book_num"],
            title=book["title"],
            author=book["author"],
            price_new=book["price_new"],
            price_old=book["price_old"],
            discount=book["discount"],
            rating=book["rating"],
            image=book["image"],
        )

        self.async_session.add(new_book)
        await self.async_session.flush()

    async def update_table_book(self, book: dict, existing_book) -> None:
        existing_book.price_new = book["price_new"]
        existing_book.price_old = book["price_old"]
        existing_book.discount = book["discount"]
        existing_book.rating = book["rating"]

        await self.async_session.flush()


class HistoryHandler:
    def __init__(self, async_session):
        self.async_session = async_session

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
