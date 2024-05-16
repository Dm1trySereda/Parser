from src.config.database.db_helpers import db_helper
from sqlalchemy import exists, insert, select
from src.models.books_models import Book
from src.models.books_history_models import BooksHistory


class BaseHandler:
    def __init__(self):
        self.db_helper = db_helper

    async def process_books(self, pages: list) -> None:
        async with self.db_helper.get_db_session() as async_session:
            for books in pages:
                for book in books:
                    stmt = select(Book).where(Book.book_num == book["book_num"])
                    result = await async_session.execute(stmt)
                    existing_book = result.scalars().first()
                    if existing_book:
                        await BookHandler(async_session).update_book(
                            book, existing_book
                        )
                    else:
                        await BookHandler(async_session).add_book(book)

            await async_session.commit()


class BookHandler:
    def __init__(self, session):
        self.async_session = session

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

    async def update_book(self, book: dict, existing_book) -> None:
        existing_book.price_new = book["price_new"]
        existing_book.price_old = book["price_old"]
        existing_book.discount = book["discount"]
        existing_book.rating = book["rating"]
        await self.async_session.flush()


class BookHistoryHandler(BaseHandler):

    async def update_books_history(self):
        async with self.db_helper.get_db_session() as async_session:
            stmt = insert(BooksHistory).from_select(
                ["book_id", "date", "book_num", "title", "price"],
                select(
                    Book.id, Book.date, Book.book_num, Book.title, Book.price_new
                ).where(
                    ~exists()
                    .where(BooksHistory.book_num == Book.book_num)
                    .where(BooksHistory.price == Book.price_new)
                ),
            )
            await async_session.execute(stmt)
            await async_session.commit()
