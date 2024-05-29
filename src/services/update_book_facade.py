from fastapi import HTTPException, status

from src.services.search_book_services.abc import AbstractSearchBookService
from src.services.update_book_services.abc import AbstractUpdateBookService
from src.services.update_history_services.abc import AbstractUpdateHistoryService


class UpdateBookFacade:
    def __init__(
        self,
        searcher_services: AbstractSearchBookService,
        updater_services: AbstractUpdateBookService,
        history_updater_services: AbstractUpdateHistoryService,
    ):
        self.searcher = searcher_services
        self.updater = updater_services
        self.history_inserter = history_updater_services

    async def update_book(self, book):
        existing_book = await self.searcher.search(book_num=book.book_num)
        if existing_book:
            update_book = await self.updater.update(*existing_book, book)
            await self.history_inserter.update_history()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return update_book
