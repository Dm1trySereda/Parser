from sqlalchemy import Result, and_, asc, delete, desc, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.models.books import Book


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SelectBook(BaseRepository):
    async def select_book(self, **kwargs) -> Result[tuple[Book]]:
        select_values = list()

        if kwargs.get("book_id"):
            select_values.append(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            select_values.append(Book.book_num == kwargs.get("book_num"))
        if kwargs.get("title"):
            select_values.append(Book.title.contains(kwargs.get("title")))
        if kwargs.get("author"):
            select_values.append(Book.author.contains(kwargs.get("author")))
        if kwargs.get("price_new"):
            select_values.append(Book.price_new == kwargs.get("price_new"))
        if kwargs.get("price_old"):
            select_values.append(Book.price_old == kwargs.get("price_old"))
        if kwargs.get("discount"):
            select_values.append(Book.discount == kwargs.get("discount"))
        if kwargs.get("rating"):
            select_values.append(Book.rating == kwargs.get("rating"))
        if kwargs.get("image"):
            select_values.append(Book.image == kwargs.get("image"))

        stmt = select(Book).where(and_(*select_values))
        return await self.async_session.execute(stmt)


class Paginate:
    def __init__(self, session: AsyncSession):
        self.async_session = session

    async def select_books(
        self, page: int, books_quantity: int, sort_by: SortChoices, order_asc: bool
    ) -> Result[tuple[Book]]:
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = (
            getattr(Book, sort_by.value) if hasattr(Book, sort_by.value) else Book.title
        )
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        stmt = (
            select(Book).limit(books_quantity).offset(books_offset).order_by(sort_order)
        )
        return await self.async_session.execute(stmt)


class InsertBook(BaseRepository):
    async def insert_new_book(self, new_book: dict):
        new_book = Book(
            book_num=new_book.get("book_num"),
            title=new_book.get("title"),
            author=new_book.get("author"),
            price_new=new_book.get("price_new"),
            price_old=new_book.get("price_old"),
            discount=new_book.get("discount"),
            rating=new_book.get("rating"),
            image=new_book.get("image_url"),
        )
        self.async_session.add(new_book)
        return new_book


class UpdateBook(BaseRepository):
    async def update_book(self, current_book: Book, book: dict):
        update_values = {
            "title": book.get("title"),
            "author": book.get("author"),
            "rating": book.get("rating"),
            "image": book.get("image_url"),
        }

        new_price = book.get("price_new")
        if new_price is not None:
            new_price = float(new_price)
            old_price = float(current_book.price_new)
            update_values["price_new"] = new_price
            update_values["price_old"] = old_price
            update_values["discount"] = (
                f"{round(((old_price - new_price) / old_price * 100))}%"
            )

        stmt = (
            update(Book)
            .where(Book.book_num == book.get("book_num"))
            .values(**update_values)
        )
        await self.async_session.execute(stmt)
        return current_book


class DeleteBook(BaseRepository):

    async def delete_book(self, current_book, **kwargs):
        select_values = list()
        if kwargs.get("book_id"):
            select_values.append(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            select_values.append(Book.book_num == kwargs.get("book_num"))

        stmt = delete(Book).where(*select_values)
        await self.async_session.execute(stmt)
        return current_book


class DeleteDuplicateBooks(BaseRepository):

    async def remove_duplicates(self):
        select_all = select(Book)
        result_all = await self.async_session.execute(select_all)
        all_books = result_all.scalars().all()

        book_counts = {}

        for book in all_books:
            if book.book_num in book_counts:
                book_counts[book.book_num] += 1
            else:
                book_counts[book.book_num] = 1
        for book_num, count in book_counts.items():
            if count > 1:
                duplicates_query = select(Book).where(Book.book_num == book_num)
                result_duplicates = await self.async_session.execute(duplicates_query)
                duplicates = result_duplicates.scalars().all()

                for duplicate in duplicates[1:]:
                    stmt = delete(Book).where(Book.id == duplicate.id)
                    await self.async_session.execute(stmt)
