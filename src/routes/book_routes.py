from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Query, status
from starlette.requests import Request

from src.repositories.books_api_actions import (
    DeleteHistory,
    InsertBook,
    Paginate,
    SearchBook,
    UpdateBook,
)
from src.schemas.books import BookIn, BookOuts

book_router = APIRouter(tags=["Books"])


@book_router.get(
    "/search",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=BookOuts,
    response_model_exclude_unset=True,
)
async def search_books(
        request: Request,
        book_id: Annotated[
            int, Query(alias="id", title="Search book for id in db", qe=1)
        ] = None,
        book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
        title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
):
    book_searcher = SearchBook(request.state.db)
    book = await book_searcher.select_book(book_id, book_num, title)
    result = BookOuts.from_orm(book)
    return result.dict(by_alias=False)


@book_router.get(
    "/books/",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
    response_model_exclude_unset=True,
)
async def get_books_on_page(
        request: Request,
        page: Annotated[int, Query(qe=1)] = 1,
        books_quantity: Annotated[int, Query(qe=10)] = None,
        sort_by: Annotated[str, Query()] = "title",
        order_asc: Annotated[bool, Query()] = False,
):
    book_paginator = Paginate(request.state.db)
    books = await book_paginator.select_books(page, books_quantity, sort_by, order_asc)
    result = [BookOuts.from_orm(book).dict(by_alias=False) for book in books]
    return result


@book_router.put(
    "/books/update",
    status_code=status.HTTP_200_OK,
    response_model=BookIn,
    response_model_exclude_unset=True,
    response_description="Book updated",
)
async def change_book(request: Request, book: Annotated[BookIn, Body(embed=True)]):
    if book.book_num == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid book number"
        )
    book_updater = UpdateBook(request.state.db)
    await book_updater.update_book(book.dict())
    return book


@book_router.post(
    "/books/add",
    status_code=status.HTTP_201_CREATED,
    response_model=BookIn,
    response_model_exclude_unset=True,
    response_description="Book added",
)
async def add_book(request: Request, new_book: Annotated[BookIn, Body(embed=True)]):
    if new_book.book_num == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Invalid book number"
        )
    book_inserter = InsertBook(request.state.db)
    await book_inserter.insert_new_book(new_book.dict())
    return new_book


@book_router.delete(
    "/books/delete",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Book deleted",
    response_model=BookOuts,
    response_model_exclude_unset=True,
)
async def delete_book(
        request: Request,
        book_id: Annotated[int, Query(qe=1)] = None,
        book_num: Annotated[int, Query(qe=100)] = None,
):
    book_deleter = DeleteHistory(request.state.db)
    select_book = SearchBook(request.state.db)
    book = await select_book.select_book(book_id)
    await book_deleter.delete_history(book_id, book_num)
    result = BookOuts.from_orm(book)
    return result.dict(by_alias=False)
