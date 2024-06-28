from pydantic import TypeAdapter
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.books import SelectBook
from src.response_schemas.books import BookOuts
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
        author: str = None,
        price_new: float = None,
        price_old: float = None,
        discount: str = None,
        rating: float = None,
        image: str = None,
    ) -> list[BookOuts]:
        fetched_books = await self.repository.select_book(
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
        return TypeAdapter(list[BookOuts]).validate_python(
            fetched_books.scalars().all()
        )
