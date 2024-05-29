from fastapi import HTTPException, status

from src.services.delete_book_services.abc import AbstractDeleteBookService
from src.services.search_book_services.abc import AbstractSearchBookService


class DeleteBookFacade:
    def __init__(
        self,
        search_services: AbstractSearchBookService,
        delete_services: AbstractDeleteBookService,
    ):
        self.book_searcher = search_services
        self.book_deleter = delete_services

    async def delete_book(self, **kwargs):
        if not any(kwargs.values()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        current_book = await self.book_searcher.search(**kwargs)
        if current_book:
            delete_book = await self.book_deleter.delete_book(*current_book, **kwargs)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return delete_book
