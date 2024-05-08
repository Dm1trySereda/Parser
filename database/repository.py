import asyncio
from sqlalchemy import select, func, insert, exists
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.core import async_engine
from database.models import Book, BooksHistory

async_session_manager = async_sessionmaker(async_engine)


async def update_or_insert_books(pages: list):
    async with async_session_manager() as async_session:
        for books in pages:
            for book in books:
                stmt = select(Book).where((Book.book_num == book['book_num']) & (Book.price_new == book['price']))
                result = await async_session.execute(stmt)
                existing_book = result.scalars().first()

                if existing_book:
                    existing_book.title = book['name']
                    existing_book.author = book['author']
                    existing_book.price_new = book['price']
                    existing_book.price_old = book['price_old']
                    existing_book.discount = book['discount']
                    existing_book.rating = book['rating']
                    existing_book.image = book['image']

                else:
                    new_books = Book(
                        book_num=book['book_num'],
                        title=book['name'],
                        author=book['author'],
                        price_new=book['price'],
                        price_old=book['price_old'],
                        discount=book['discount'],
                        rating=book['rating'],
                        image=book['image'],
                    )

                    async_session.add(new_books)
        await async_session.commit()


async def insert_book_history():
    async with async_session_manager() as async_session:
        stmt = (
            insert(BooksHistory)
            .from_select(
                ['book_id', 'date', 'book_num', 'title', 'price'],
                select(Book.id, Book.date, Book.book_num, Book.title, Book.price_new)
                .where(~exists().where(BooksHistory.book_id == Book.id).where(BooksHistory.price == Book.price_new))
            )
        )
        await async_session.execute(stmt)
        await async_session.commit()


def update_or_insert_books_sync(pages: list):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(update_or_insert_books(pages))


def insert_books_history_sync():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_book_history())
