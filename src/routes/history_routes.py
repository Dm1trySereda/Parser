from fastapi import APIRouter
from starlette.requests import Request

from src.repositories.books_api_actions import RepetitiveBook

history_routes = APIRouter(tags=["History"])


@history_routes.get("/history/repetitive/")
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    result = await book_repetitive.select_book_history()
    return result
