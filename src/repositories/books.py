from sqlalchemy import Result, asc, delete, desc, select, update, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from src.enums.book import SortChoices
from src.models.books import Book
from src.response_schemas.books import BookOuts


class BaseRepository:
    def __init__(self, session: AsyncSession):
        self.async_session = session


class SelectBook(BaseRepository):
    async def select_book(self, **kwargs) -> Result[tuple[Book]]:
        query = select(Book)

        if kwargs.get("book_id"):
            query = query.filter(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            query = query.filter(Book.book_num == kwargs.get("book_num"))
        if kwargs.get("title"):
            query = query.filter(Book.title.contains(kwargs.get("title")))
        if kwargs.get("authors"):
            author_filters = [
                Book.author.contains(author) for author in kwargs.get("authors")
            ]
            query = query.filter(or_(*author_filters))
        if kwargs.get("price_new"):
            query = query.filter(Book.price_new == kwargs.get("price_new"))
        if kwargs.get("price_old"):
            query = query.filter(Book.price_old == kwargs.get("price_old"))
        if kwargs.get("discount"):
            query = query.filter(Book.discount == kwargs.get("discount"))
        if kwargs.get("rating"):
            query = query.filter(Book.rating == kwargs.get("rating"))
        if kwargs.get("image"):
            query = query.filter(Book.image == kwargs.get("image"))
        if kwargs.get("years"):
            query = query.filter(Book.year.in_(kwargs.get("years")))
        return await self.async_session.execute(query)

    async def get_most_popular_authors(self):
        count_books = func.count(Book.title).label("count")
        query = (
            select(Book.author.label("author"), count_books)
            .where(~Book.author.op("REGEXP")("^[0-9]+$"))
            .group_by("author")
            .order_by(desc("count"))
        )
        return await self.async_session.execute(query)

    async def get_publishing_year(self):
        count_books = func.count(Book.id).label("count")
        query = (
            select(Book.year.label("year"), count_books)
            .group_by("year")
            .order_by(desc("year"))
        )
        return await self.async_session.execute(query)


class Paginate(BaseRepository):

    async def select_books(
        self,
        page: int,
        books_quantity: int,
        sort_by: SortChoices,
        order_asc: bool,
        authors: list,
        years: list,
    ) -> Result[tuple[Book]]:
        query = select(Book)
        if authors:
            author_filters = [Book.author.contains(author) for author in authors]
            query = query.filter(or_(*author_filters))
        if years:
            query = query.filter(Book.year.in_(years))
        books_quantity = books_quantity or 10
        books_offset = (page - 1) * books_quantity
        sort_params = (
            getattr(Book, sort_by.value) if hasattr(Book, sort_by.value) else Book.title
        )
        sort_order = asc(sort_params) if order_asc else desc(sort_params)
        query = query.limit(books_quantity).offset(books_offset).order_by(sort_order)
        return await self.async_session.execute(query)


class InsertBook(BaseRepository):
    async def insert_new_book(self, new_book: dict) -> Book:
        new_book = Book(
            book_num=new_book.get("book_num"),
            title=new_book.get("title"),
            author=new_book.get("author"),
            year=new_book.get("year"),
            price_new=new_book.get("price_new"),
            price_old=new_book.get("price_old"),
            discount=new_book.get("discount"),
            rating=new_book.get("rating"),
            image=new_book.get("image_url"),
        )
        self.async_session.add(new_book)
        return new_book


class UpdateBook(BaseRepository):
    async def update_book(self, existing_book: BookOuts, current_book: dict) -> Book:
        update_values = {
            "title": current_book.get("title"),
            "author": current_book.get("author"),
            "rating": current_book.get("rating"),
            "image": current_book.get("image_url"),
        }

        new_price = current_book.get("price_new")
        if new_price:
            new_price = float(new_price)
            old_price = float(existing_book.price_new)
            update_values["price_new"] = new_price
            update_values["price_old"] = old_price
            update_values["discount"] = (
                f"{round(((old_price - new_price) / old_price * 100))}%"
            )

        stmt = (
            update(Book)
            .where(Book.book_num == current_book.get("book_num"))
            .values(**update_values)
        )
        await self.async_session.execute(stmt)
        updated_book = await self.async_session.scalar(
            select(Book).where(Book.book_num == current_book.get("book_num"))
        )
        return updated_book


class DeleteBook(BaseRepository):

    async def delete_book(self, existing_book: BookOuts, **kwargs) -> BookOuts:
        query = delete(Book)
        if kwargs.get("book_id"):
            query = query.filter(Book.id == kwargs.get("book_id"))
        if kwargs.get("book_num"):
            query = query.filter(Book.book_num == kwargs.get("book_num"))
        await self.async_session.execute(query)
        return existing_book
