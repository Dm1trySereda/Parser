from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.requests import Request
from starlette.responses import Response

from src.config.database.db_configs import async_engine
from src.parser.repository import (DeleteBookHistory, InsertBook, Paginate,
                                   RepetitiveBook, SearchBook, UpdateBook)

async_session_manager = async_sessionmaker(async_engine)
app = FastAPI(
    title="OZ Books App",
)
templates = Jinja2Templates(directory="src/parser/templates")


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        # Создаем новую сессию и если все ок - подтверждаем транзакцию
        request.state.db = async_session_manager()
        response = await call_next(request)
        await request.state.db.commit()
    except Exception as exc:
        # Если что-то пошло не так, откатываем транзакцию и возвращаем ответ клиенту
        await request.state.db.rollback()
        raise exc
    finally:
        # Закрываем сессию, когда запрос завершен
        await request.state.db.close()
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
    book_deleter = DeleteBookHistory(request.state.db)
    await book_deleter.delete_book_history(book_id, book_num)
    return {"Delete book": "OK"}


@app.get("/books_history/repetitive/", tags=["Repetitive"])
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    result = await book_repetitive.select_book_history()
    return result
