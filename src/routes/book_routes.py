from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, Query, status
from starlette.requests import Request

from src.enums.book import SortChoices
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.response_schemas.users import UserResponse
from src.services.add_new_book_facade import AddNewBookFacade
from src.services.auth_services.auth_user import get_current_active_user
from src.services.paginate_facade import PaginationFacade
from src.services.search_book_facade import BookSearchFacadeServices
from src.services.update_book_facade import UpdateBookFacade
from src.services.delete_book_fasade import DeleteBookFacade

book_router = APIRouter(tags=["Books"])


@book_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
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
    facade = BookSearchFacadeServices(request.state.db)
    search_result = await facade.search_book(
        book_id=book_id, book_num=book_num, title=title, author=author
    )
    return [BookOuts.parse_obj(books.__dict__) for books in search_result]


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
    paginator = PaginationFacade(request.state.db)
    page = await paginator.paginate(
        page=page, books_quantity=books_quantity, sort_by=sort_by, order_asc=order_asc
    )

    return [BookOuts.parse_obj(books.__dict__) for books in page]


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
    book_inserter = AddNewBookFacade(request.state.db)
    new_book = await book_inserter.add_new_book(new_book)
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
    book_updater = UpdateBookFacade(request.state.db)
    updated_book = await book_updater.update_book(book)
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
    book_deleter = DeleteBookFacade(request.state.db)
    book = await book_deleter.delete_book(book_id=book_id, book_num=book_num)
    return book
