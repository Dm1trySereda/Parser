from fastapi import APIRouter
from starlette.requests import Request

from src.repositories.books_api_actions import (
    DeleteHistory,
    InsertBook,
    Paginate,
    RepetitiveBook,
    SearchBook,
    UpdateBook,
)
from src.schemas.books import Book

book_router = APIRouter(tags=["Books"])


@book_router.get("/search")
async def search_books(
    request: Request, book_id: int = None, book_num: int = None, title: str = None
):
    book_searcher = SearchBook(request.state.db)
    result = await book_searcher.select_book(book_id, book_num, title)
    return result


@book_router.get("/books/")
async def get_books_on_page(
    request: Request,
    page: int = 1,
    books_quantity: int = None,
    sort_by: str = "title",
    order_asc: bool = False,
):
    book_paginator = Paginate(request.state.db)
    result = await book_paginator.select_books(page, books_quantity, sort_by, order_asc)
    return result


@book_router.post("/books/change")
async def change_book(request: Request, book: Book):
    book_updater = UpdateBook(request.state.db)
    await book_updater.update_book(book.dict())

    return {
        "Update book": "Success",
    }


@book_router.post("/books/add")
async def add_book(request: Request, new_book: Book):
    book_inserter = InsertBook(request.state.db)
    await book_inserter.insert_new_book(new_book.dict())
    return {
        "Add book": "Success",
    }


@book_router.delete("/books/delete")
async def delete_book(request: Request, book_id: int = None, book_num: int = None):
    book_deleter = DeleteHistory(request.state.db)
    await book_deleter.delete_history(book_id, book_num)
    return {"Delete book": "OK"}
