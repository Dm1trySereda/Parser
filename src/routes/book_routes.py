from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from starlette.requests import Request

from src.enums.book import SortChoices
from src.repository.parser_handler.history import HistoryRepository
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.response_schemas.users import UserResponse
from src.services.add_new_book_services.repository import (
    AbstractAddNewBookService,
    RepositoryAddNewBookService,
)
from src.services.auth_services.auth_user import get_current_active_user
from src.services.delete_book_services.repository import (
    AbstractDeleteBookService,
    RepositoryDeleteBookService,
)
from src.services.paginate_book_services.repository import (
    AbstractPaginateBookService,
    RepositoryPaginateBookService,
)
from src.services.search_book_services.repository import (
    AbstractSearchBookService,
    RepositorySearchBookService,
)
from src.services.update_book_services.repository import (
    AbstractUpdateBookService,
    RepositoryUpdateBookService,
)
from src.validation.book_validates import (
    validate_inserter,
    validate_parameters,
    validate_searcher,
)

book_router = APIRouter(tags=["Books"])


@book_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=BookOuts | list[BookOuts],
)
async def search_books(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    book_id: Annotated[
        int, Query(alias="id", title="Search book for id in db", qe=1)
    ] = None,
    book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
    title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
    author: Annotated[str, Query(title="Search book for author", min_length=3)] = None,
) -> BookOuts | list[BookOuts]:
    search_service: AbstractSearchBookService = RepositorySearchBookService(
        request.state.db
    )
    try:
        validate_parameters(
            book_id=book_id, bok_num=book_num, title=title, author=author
        )
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    search_result = await search_service.search(
        book_id=book_id, book_num=book_num, title=title, author=author
    )
    try:
        validate_searcher(search_book=search_result)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return (
        [BookOuts.parse_obj(books.__dict__) for books in search_result]
        if isinstance(search_result, list)
        else BookOuts.parse_obj(search_result.__dict__)
    )


@book_router.get(
    "/books/",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
)
async def get_books_on_page(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    page: Annotated[int, Query(qe=1)] = 1,
    books_quantity: Annotated[int, Query(qe=10)] = None,
    sort_by: Annotated[SortChoices, Query()] = SortChoices.title,
    order_asc: Annotated[bool, Query()] = False,
) -> list[BookOuts]:
    try:
        validate_parameters(
            page=page,
            books_quantity=books_quantity,
            sort_by=sort_by,
            order_asc=order_asc,
        )
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    paginate_service: AbstractPaginateBookService = RepositoryPaginateBookService(
        request.state.db
    )
    books = await paginate_service.paginate(
        page=page, books_quantity=books_quantity, sort_by=sort_by, order_asc=order_asc
    )
    try:
        validate_searcher(search_book=books)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return [BookOuts.parse_obj(book.__dict__) for book in books]


@book_router.post(
    "/books/add",
    status_code=status.HTTP_201_CREATED,
    response_model=BookOuts,
    response_description="Book added",
)
async def add_book(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    new_book: Annotated[BookIn, Body(embed=False)],
):
    book_inserter: AbstractAddNewBookService = RepositoryAddNewBookService(
        request.state.db
    )
    history_handler = HistoryRepository(request.state.db)
    new_book = await book_inserter.add_new_book(new_book)
    try:
        validate_inserter(new_book)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    await history_handler.update_books_history()
    return new_book


@book_router.put(
    "/books/update",
    status_code=status.HTTP_200_OK,
    response_model=BookOuts,
    response_description="Book updated",
)
async def change_book(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    book: Annotated[BookIn, Body(embed=False)],
):
    book_updater: AbstractUpdateBookService = RepositoryUpdateBookService(
        request.state.db
    )
    history_handler = HistoryRepository(request.state.db)

    updated_book = await book_updater.update(book)
    try:
        validate_inserter(updated_book)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    await history_handler.update_books_history()
    return updated_book


@book_router.delete(
    "/books/delete",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Book deleted",
    response_model=BookOuts,
)
async def delete_book(
    request: Request,
    current_user: Annotated[UserResponse, Depends(get_current_active_user)],
    book_id: Annotated[int, Query(qe=1)] = None,
    book_num: Annotated[int, Query(qe=100)] = None,
):
    book_deleter: AbstractDeleteBookService = RepositoryDeleteBookService(
        request.state.db
    )
    try:
        validate_parameters(book_id=book_id, book_num=book_num)
    except AttributeError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    book = await book_deleter.delete_book(book_id=book_id, book_num=book_num)
    try:
        validate_searcher(book)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return book
