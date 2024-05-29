from fastapi import HTTPException, status

from src.services.add_new_book_services.abc import AbstractAddNewBookService
from src.services.search_book_services.abc import AbstractSearchBookService
from src.services.update_history_services.abc import AbstractUpdateHistoryService


class AddNewBookFacade:
    def __init__(
        self,
        search_services: AbstractSearchBookService,
        inserter_services: AbstractAddNewBookService,
        history_updater_services: AbstractUpdateHistoryService,
    ):
        self.searcher = search_services
        self.inserter = inserter_services
        self.history_inserter = history_updater_services

    async def add_new_book(self, new_book):
        current_books = await self.searcher.search(book_num=new_book.book_num)
        if not current_books:
            new_book_record = await self.inserter.add_new_book(new_book)
            await self.history_inserter.update_history()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book already exist"
            )
        return new_book_record
