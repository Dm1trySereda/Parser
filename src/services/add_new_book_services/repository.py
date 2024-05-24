from typing import Any, Coroutine

from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Book
from src.repository.api_action.books import InsertBook
from src.request_shemas.books import BookIn
from src.services.add_new_book_services.abc import AbstractAddNewBookService
from src.services.search_book_services.repository import RepositorySearchBookService


class RepositoryAddNewBookService(AbstractAddNewBookService):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.search_service = RepositorySearchBookService(session)

    async def add_new_book(self, new_book: BookIn) -> Book | Any:
        current_book = await self.search_service.search(book_num=new_book.book_num)
        if current_book is None:
            inserter = InsertBook(self.session)
            new_book_record = await inserter.insert_new_book(new_book=new_book.model_dump(by_alias=False))
            await self.session.flush([new_book_record])
            await self.session.refresh(new_book_record)
            return new_book_record
        return None
