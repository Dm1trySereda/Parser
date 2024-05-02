from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from FastAPI.repository import select_books, select_books_search

app = FastAPI()
templates = Jinja2Templates(directory="FastAPI/templates")


@app.get("/")
async def read_root():
    return {"Hello": "World"}


#
# Пагинация
@app.get("/books/", response_class=HTMLResponse)
async def read_root(request: Request, page: int = 1):
    library = await select_books(page)
    return templates.TemplateResponse('books.html', {"request": request, "library": library, "page": page})


#
# Поиск книги
@app.get("/search", response_class=HTMLResponse)
async def search_books(request: Request, name: str = None):
    library = await select_books_search(name)
    return templates.TemplateResponse('books.html', {"request": request, "library": library, "page": 1})
