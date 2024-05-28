from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.history import UpdateHistory
from src.services.search_book_services.repository import (
    AbstractSearchBookService,
    RepositorySearchBookService,
)
from src.services.update_book_services.repository import (
    AbstractUpdateBookService,
    RepositoryUpdateBookService,
)


class UpdateBookFacade:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher: AbstractSearchBookService = RepositorySearchBookService(session)
        self.updater: AbstractUpdateBookService = RepositoryUpdateBookService(session)
        self.history_inserter = UpdateHistory(session)

    async def update_book(self, book):
        existing_book = await self.searcher.search(book_num=book.book_num)
        if existing_book:
            update_book = await self.updater.update(*existing_book, book)
            await self.history_inserter.update_books_history()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return update_book
