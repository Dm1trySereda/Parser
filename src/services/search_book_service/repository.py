from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.books import SelectBook
from src.response_schemas.books import BookOuts, PopularAuthor, PublishingYear
from src.services.search_book_service.abc import AbstractSearchBookService


class RepositorySearchBookService(AbstractSearchBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = SelectBook(session)

    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        authors: list = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
        years: list = None,
    ) -> list[BookOuts]:
        fetched_books = await self.repository.select_book(
            book_id=book_id,
            book_num=book_num,
            title=title,
            authors=authors,
            price_new=price_new,
            price_old=price_old,
            discount=discount,
            rating=rating,
            image=image,
            years=years,
        )
        return TypeAdapter(list[BookOuts]).validate_python(
            fetched_books.scalars().all()
        )

    async def search_popular(self, count: int = 10):
        popular_books = await self.repository.get_most_popular_authors()
        return TypeAdapter(list[PopularAuthor]).validate_python(
            popular_books.fetchall()[0:count]
        )

    async def search_publishing_year(self, count: int = 10):
        publishing_year_books = await self.repository.get_publishing_year()
        return TypeAdapter(list[PublishingYear]).validate_python(
            publishing_year_books.fetchall()[0:count]
        )
