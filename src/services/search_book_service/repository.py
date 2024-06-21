from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import Book
from src.repositories.books import SelectBook
from src.services.search_book_service.abc import AbstractSearchBookService


class RepositorySearchBookService(AbstractSearchBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher = SelectBook(session)

    async def search(
        self,
        book_id: int = None,
        book_num: int = None,
        title: str = None,
        author: str = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
    ) -> Sequence[Book] | None:
        fetched_books = await self.searcher.select_book(
            book_id=book_id,
            book_num=book_num,
            title=title,
            author=author,
            price_new=price_new,
            price_old=price_old,
            discount=discount,
            rating=rating,
            image=image,
        )
        return fetched_books.scalars().all()
