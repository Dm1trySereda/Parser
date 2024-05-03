import asyncio
from sqlalchemy import select, func, insert, exists
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.core import async_engine
from database.models import Book, BooksHistory

async_session_manager = async_sessionmaker(async_engine)


async def insert_books(read_pages: list):
    async with async_session_manager() as async_session:
        for line in read_pages:
            for page, books in line.items():
                for book in books:
                    stmt = select(Book).where(Book.book_num == book['book_num'])
                    result = await async_session.execute(stmt)
                    existing_book = result.scalar_one_or_none()

                    book_num = book['book_num']
                    title = book['name']
                    author = book['author']
                    price_new = book['price']
                    price_old = book['price_old']
                    discount = book['discount']
                    rating = book['rating']
                    image = book['image']

                    # Если книга не существует - добавляем
                    if existing_book is None:
                        books = Book(
                            book_num=book_num,
                            title=title,
                            author=author,
                            price_new=price_new,
                            price_old=price_old,
                            discount=discount,
                            rating=rating,
                            image=image,
                        )
                        async_session.add(books)
                        # Если книга существует - сравниваем цену в бд и данных парсера, если отличается - обновляем цену
                    else:
                        if existing_book.price_new != price_new:
                            existing_book.title = title
                            existing_book.author = author
                            existing_book.price_new = price_new
                            existing_book.price_old = price_old
                            existing_book.discount = discount
                            existing_book.rating = rating
                            existing_book.image = image

        await async_session.commit()


def insert_books_sync(read_pages: list):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_books(read_pages))


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


def insert_books_history_sync():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(insert_book_history())
