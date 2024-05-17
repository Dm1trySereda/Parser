from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

from src.config.database.db_helpers import db_helper
from src.repositories.books_api_actions import (
    DeleteHistory,
    InsertBook,
    Paginate,
    RepetitiveBook,
    SearchBook,
    UpdateBook,
)

app = FastAPI(
    title="OZ Books App",
)
templates = Jinja2Templates(directory="src/templates")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    async with db_helper.get_db_session() as session:
        request.state.db = session
        response = await call_next(request)
    return response


@app.get("/", tags=["Search"])
async def search_books(
    request: Request, book_id: int = None, book_num: int = None, title: str = None
):
    book_searcher = SearchBook(request.state.db)
    result = await book_searcher.select_book(book_id, book_num, title)
    return result


@app.get("/books/", tags=["Pagination"])
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


@app.post("/books/change", tags=["Change book"])
async def change_book(
    request: Request,
    book_num: int,
    new_title: str = None,
    new_author: str = None,
    new_price: float = None,
    new_rating: float = None,
    new_image: str = None,
):
    book_updater = UpdateBook(request.state.db)
    await book_updater.update_book(
        book_num, new_title, new_author, new_price, new_rating, new_image
    )
    return {
        "Update book": "OK",
        "New title": new_title,
        "New author": new_author,
        "New price": new_price,
        "New image": new_image,
    }


@app.post("/books/add", tags=["Add book"])
async def add_book(
    request: Request,
    book_num: int,
    title: str,
    author: str,
    price: float,
    rating: float,
    image: str,
):
    book_inserter = InsertBook(request.state.db)
    await book_inserter.insert_new_book(book_num, title, author, price, rating, image)
    return {
        "Add book": "OK",
        "Title": title,
        "Author": author,
        "Price": price,
        "Rating": rating,
        "Image": image,
    }


@app.delete("/books/delete", tags=["Delete book"])
async def delete_book(request: Request, book_id: int = None, book_num: int = None):
    book_deleter = DeleteHistory(request.state.db)
    await book_deleter.delete_history(book_id, book_num)
    return {"Delete book": "OK"}


@app.get("/books_history/repetitive/", tags=["Repetitive"])
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    result = await book_repetitive.select_book_history()
    return result
