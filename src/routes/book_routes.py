from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, status
from starlette.requests import Request

from src.enums.book import SortChoices
from src.repositories.api_action.books import (
    BaseRepository,
    DeleteBook,
    InsertBook,
    Paginate,
    UpdateBook,
)
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts

book_router = APIRouter(tags=["Books"])


# class AuthService:
#     def __init__(self, auth_service_url: str, api_key: str):
#         self.auth_service_url = auth_service_url
#         self.api_key = api_key
#
#     async def validate_token(self, token: str) -> dict:
#         ...
#
#
# def auth_service_factory() -> AuthService:
#     return AuthService(setting_db.AUTH_SERVICE_URL, setting_db.AUTH_SERVICE_API_KEY)
#
#
# auth_service_dependency = Annotated[AuthService, Depends(auth_service_factory)]
#
#
# async def auth(authorization: Annotated[str, Header()], auth_service: auth_service_dependency) -> dict:
#     try:
#         user_info = await auth_service.validate_token(authorization)
#         return user_info
#     except Exception:
#         raise HTTPException(HTTPStatus.UNAUTHORIZED)
#
# user_info_dependency = Annotated[dict, Depends(auth)]
def validate_parameters(**kwargs):
    if not any(kwargs.values()):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You need to specify at least one parameter",
        )


def validate_searcher(search_book):
    if not search_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Page not found"
        )


@book_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=BookOuts | list[BookOuts],
)
async def search_books(
    request: Request,
    book_id: Annotated[
        int, Query(alias="id", title="Search book for id in db", qe=1)
    ] = None,
    book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
    title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
) -> BookOuts | list[BookOuts]:
    validate_parameters(book_id=book_id, book_num=book_num, title=title)
    base_rep_instance = BaseRepository(request.state.db)
    search = await base_rep_instance.select_book(book_id, book_num, title)

    validate_searcher(search_book=search)
    return (
        [BookOuts.parse_obj(books.__dict__) for books in search]
        if isinstance(search, list)
        else BookOuts.parse_obj(search.__dict__)
    )


@book_router.get(
    "/books/",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
)
async def get_books_on_page(
    request: Request,
    page: Annotated[int, Query(qe=1)] = 1,
    books_quantity: Annotated[int, Query(qe=10)] = None,
    sort_by: Annotated[SortChoices, Query()] = SortChoices.title,
    order_asc: Annotated[bool, Query()] = False,
) -> list[BookOuts]:
    validate_parameters(
        page=page, books_quantity=books_quantity, sort_by=sort_by, order_asc=order_asc
    )
    book_paginator = Paginate(request.state.db)
    books = await book_paginator.select_books(page, books_quantity, sort_by, order_asc)
    validate_searcher(search_book=books)
    return [BookOuts.parse_obj(book.__dict__) for book in books]


@book_router.put(
    "/books/update",
    status_code=status.HTTP_200_OK,
    response_model=BookOuts,
    response_description="Book updated",
)
async def change_book(request: Request, book: Annotated[BookIn, Body(embed=False)]):
    if book.book_num == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid book number"
        )
    book_updater = UpdateBook(request.state.db)
    book = await book_updater.update_book(book.model_dump(by_alias=False))
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book not found"
        )
    return book


@book_router.post(
    "/books/add",
    status_code=status.HTTP_201_CREATED,
    response_model=BookOuts,
    response_description="Book added",
)
async def add_book(request: Request, new_book: Annotated[BookIn, Body(embed=False)]):
    book_inserter = InsertBook(request.state.db)
    new_book = await book_inserter.insert_new_book(new_book.model_dump(by_alias=False))
    if new_book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists"
        )
    return new_book


@book_router.delete(
    "/books/delete",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Book deleted",
    response_model=BookOuts,
)
async def delete_book(
    request: Request,
    book_id: Annotated[int, Query(qe=1)] = None,
    book_num: Annotated[int, Query(qe=100)] = None,
):
    book_deleter = DeleteBook(request.state.db)
    book = await book_deleter.delete_book(book_id, book_num)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Book already exists"
        )
    return book
