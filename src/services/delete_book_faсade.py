from fastapi import HTTPException, status

from src.response_schemas.books import BookOuts
from src.services.delete_book_service.abc import AbstractDeleteBookService
from src.services.search_book_service.abc import AbstractSearchBookService


class DeleteBookFacade:
    def __init__(
            self,
            search_services: AbstractSearchBookService,
            delete_services: AbstractDeleteBookService,
    ):
        self.book_searcher = search_services
        self.book_deleter = delete_services

    async def delete_book(self, book_id: int = None, book_num: int = None) -> BookOuts:
        if not any([book_id, book_num]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="You need to specify at least one parameter",
            )
        current_book = await self.book_searcher.search(book_id, book_num)
        if current_book:
            delete_book = await self.book_deleter.delete_book(*current_book, book_id, book_num)
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Book not found"
            )
        return delete_book
