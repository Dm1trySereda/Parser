from sqlalchemy.ext.asyncio import AsyncSession

from src.models.books import Book
from src.repository.books import InsertBook
from src.request_shemas.books import BookIn
from src.services.create_new_book_service.abc import AbstractAddNewBookService


class RepositoryAddNewBookService(AbstractAddNewBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repository = InsertBook(session)

    async def add_new_book(self, new_book: BookIn) -> Book:
        new_book_record = await self.repository.insert_new_book(
            new_book=new_book.model_dump(by_alias=False)
        )
        await self.session.flush([new_book_record])
        await self.session.refresh(new_book_record)
        return new_book_record
