from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.history import UpdateHistory
from src.services.add_new_book_services.repository import (
    AbstractAddNewBookService,
    RepositoryAddNewBookService,
)
from src.services.search_book_services.repository import (
    AbstractSearchBookService,
    RepositorySearchBookService,
)


class AddNewBookFacade:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.searcher: AbstractSearchBookService = RepositorySearchBookService(session)
        self.inserter: AbstractAddNewBookService = RepositoryAddNewBookService(session)
        self.history_inserter = UpdateHistory(session)

    async def add_new_book(self, new_book):
        current_books = await self.searcher.search(book_num=new_book.book_num)
        if not current_books:
            new_book_record = await self.inserter.add_new_book(new_book)
            await self.session.flush([new_book_record])
            await self.session.refresh(new_book_record)
            await self.history_inserter.update_books_history()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book already exist"
            )
        return new_book_record
