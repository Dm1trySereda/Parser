from sqlalchemy import select, func, insert, not_, exists, update, delete
from sqlalchemy.ext.asyncio import async_sessionmaker
from database.core import async_engine
from database.models import Book, BooksHistory

async_session_manager = async_sessionmaker(async_engine)


class BaseSession:
    def __init__(self):
        self.async_session_manager = async_session_manager

    @staticmethod
    async def get_books(books):
        result = []
        for book in books:
            result.append(book[0])
        return result


class SearchBook(BaseSession):

    async def select_for_id(self, book_id: int):
        async with self.async_session_manager() as async_session:
            stmt = (
                select(Book)
                .where(Book.id == book_id)
            )
            result = await async_session.execute(stmt)
            return await self.get_books(result)

    async def select_for_book_num(self, book_num: int):
        async with self.async_session_manager() as async_session:
            stmt = (
                select(Book)
                .where(Book.book_num == book_num)
            )
            result = await async_session.execute(stmt)
            return await self.get_books(result)

    async def select_for_name(self, name: str):
        async with self.async_session_manager() as async_session:
            stmt = (
                select(Book)
                .where(Book.title.contains(f"{name}"))
            )
            result = await async_session.execute(stmt)
            return await self.get_books(result)


class UpdateBook(BaseSession):
    async def update_book(self, book_num: int, new_title: str = None, new_author: str = None, new_price: float = None,
                          new_rating: float = None, new_image: str = None):
        update_values = dict()
        if new_title is not None:
            update_values['title'] = new_title
        if new_author is not None:
            update_values['author'] = new_author
        if new_price is not None:
            update_values['price_new'] = new_price
        if new_rating is not None:
            update_values['rating'] = new_rating
        if new_image is not None:
            update_values['image'] = new_image
        async with self.async_session_manager() as async_session:
            stmt = (
                update(Book)
                .where(Book.book_num == book_num)
                .values(**update_values)
            )
            await async_session.execute(stmt)
            await async_session.commit()

    async def insert_new_book(self, book_num: int, title: str, author: str, price: float, rating: float, image: str):
        async with self.async_session_manager() as async_session:
            stmt = (
                select(Book)
                .where(Book.book_num == book_num)
            )
            result = await async_session.execute(stmt)
            existing_book = result.scalars().first()
            if existing_book is None:
                new_book = Book(
                    book_num=book_num,
                    title=title,
                    author=author,
                    price_new=price,
                    rating=rating,
                    image=image,
                )
                async_session.add(new_book)
            else:
                await self.update_book(book_num=book_num, new_title=title, new_author=author, new_price=price,
                                       new_rating=rating,
                                       new_image=image)
            await async_session.commit()


class DeleteBook(BaseSession):
    async def delete_book(self, book_id: int = None, book_num: int = None):
        async with self.async_session_manager() as async_session:
            if book_id is not None:
                stmt = (
                    delete(BooksHistory)
                    .where(BooksHistory.book_id == book_id)
                )
                await async_session.execute(stmt)
                stmt = (
                    delete(Book)
                    .where(Book.id == book_id)
                )
                await async_session.execute(stmt)

            if book_num is not None:
                stmt = (
                    delete(BooksHistory)
                    .where(BooksHistory.book_num == book_num)
                )
                await async_session.execute(stmt)
                stmt = (
                    delete(Book)
                    .where(Book.book_num == book_num)
                )
                await async_session.execute(stmt)

            await async_session.commit()


class Paginate(BaseSession):
    async def select_books(self, page: int):
        books_limit = 10
        books_offset = (page - 1) * books_limit
        async with self.async_session_manager() as async_session:
            stmt = (
                select(Book)
                .order_by(Book.title)
                .limit(books_limit)
                .offset(books_offset)
            )
            result = await async_session.execute(stmt)
            return await self.get_books(result)
