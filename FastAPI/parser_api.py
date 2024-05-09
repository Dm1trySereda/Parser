from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from FastAPI.repository import *

app = FastAPI(
    title='OZ Books App',

)
templates = Jinja2Templates(directory="FastAPI/templates")


@app.get("/", tags=["Search"])
async def search_books(id: int = None, book_num: int = None, name: str = None):
    book_searcher = SearchBook()
    if id is not None:
        result = await book_searcher.select_for_id(id)
    elif book_num is not None:
        result = await book_searcher.select_for_book_num(book_num)
    else:
        result = await book_searcher.select_for_name(name)
    return result


@app.get("/books/", tags=["Pagination"])
async def get_books_on_page(page: int = 1):
    book_paginator = Paginate()
    result = await book_paginator.select_books(page)
    return result


@app.post("/books/change", tags=["Change book"])
async def change_book(book_num: int, new_title: str = None, new_author: str = None, new_price: float = None,
                      new_rating: float = None, new_image: str = None):
    book_updater = UpdateBook()
    await book_updater.update_book(book_num, new_title, new_author, new_price, new_rating, new_image)
    return {"Update book": "OK", "New title": new_title, "New author": new_author, "New price": new_price,
            "New image": new_image}


@app.post("/books/add", tags=["Add book"])
async def add_book(book_num: int, title: str, author: str, price: float, rating: float, image: str):
    book_inserter = UpdateBook()
    await book_inserter.insert_new_book(book_num, title, author, price, rating, image)
    return {"Add book": "OK", "Title": title, "Author": author, "Price": price, "Rating": rating, "Image": image}


@app.delete("/books/delete", tags=["Delete book"])
async def delete_book_for_id(book_id: int = None, book_num: int = None):
    book_deleter = DeleteBook()
    await book_deleter.delete_book(book_id, book_num)
    return {"Delete book": "OK"}
