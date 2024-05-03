from sqlalchemy import select, func, insert, not_, exists
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.core import async_engine
from database.models import Book, BooksHistory

async_session_manager = async_sessionmaker(async_engine)


async def get_books(result):
    library = []
    for book in result:
        books_dict = {
            'date': book[1],
            'book_num': book[2],
            'title': book[3],
            'author': book[4],
            'price_new': book[5],
            'price_old': book[6],
            'discount': book[7],
            'rating': book[8],
            'image': book[9],
        }
        library.append(books_dict)
    return library


async def select_books(page):
    books_limit = 12
    books_offset = (page - 1) * books_limit
    async with async_session_manager() as async_session:
        stmt = (
            select(
                func.distinct(Book.id),
                Book.date,
                Book.book_num,
                Book.title,
                Book.author,
                Book.price_new,
                Book.price_old,
                Book.discount,
                Book.rating,
                Book.image,
            )
            .order_by(Book.title)
            .limit(books_limit)
            .offset(books_offset)
        )
        result = await async_session.execute(stmt)
        return await get_books(result)


async def select_books_search(name):
    async with async_session_manager() as async_session:
        stmt = (
            select(
                func.distinct(Book.id),
                Book.date,
                Book.book_num,
                Book.title,
                Book.author,
                Book.price_new,
                Book.price_old,
                Book.discount,
                Book.rating,
                Book.image,
            )
            .where(Book.title.contains(f"{name}"))
        )
        result = await async_session.execute(stmt)
        return await get_books(result)
