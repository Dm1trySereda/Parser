from fastapi import APIRouter, status
from starlette.requests import Request

from src.repositories.books_api_actions import RepetitiveBook
from src.schemas.history import HistoryOut

history_routes = APIRouter(tags=["History"])


@history_routes.get(
    "/history/repetitive/",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="History successfully",
)
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    repetitive = await book_repetitive.select_book_history()
    result = [HistoryOut.from_orm(book).dict(by_alias=False) for book in repetitive]
    return result
