from typing import Annotated

from fastapi import APIRouter, Query, status
from starlette.requests import Request

from src.repositories.api_action.history import RepetitiveBook, SearchHistory
from src.response_schemas.history import HistoryOut

history_routes = APIRouter(tags=["History"])


@history_routes.get(
    "/history/search",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="Search book history successfully",
)
async def get_history_book(
    request: Request,
    book_id: Annotated[int, Query(title="Search book for id in db", qe=1)] = None,
    book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
    title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
):
    book_searcher = SearchHistory(request.state.db)
    books_history = await book_searcher.select_book_history(book_id, book_num, title)
    result = [HistoryOut.parse_obj(book) for book in books_history]
    return result


@history_routes.get(
    "/history/repetitive/",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="History successfully",
)
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    repetitive = await book_repetitive.select_all_history()
    result = [HistoryOut.parse_obj(book).dict(by_alias=False) for book in repetitive]
    return result
