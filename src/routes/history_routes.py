from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from starlette.requests import Request
from src.response_schemas.history import HistoryOut
from src.response_schemas.users import UserResponse
from src.services.authorization_facade import verify_user
from src.services.book_price_alert_service.repository import \
    RepositoryBookPriceAlertService
from src.services.search_history_faсade import HistorySearchFacadeServices
from src.services.search_history_service.repository import \
    RepositorySearchHistoryService

history_routes = APIRouter(tags=["History"])


@history_routes.get(
    "/history/",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="History successfully",
)
async def show_history(
        request: Request,
):
    searcher = HistorySearchFacadeServices(
        search_history_service=RepositorySearchHistoryService(request.state.db),
        book_price_alert=RepositoryBookPriceAlertService(request.state.db)
    )
    cheap_books = await searcher.get_cheap_books()
    result = [
        HistoryOut.parse_obj(book.__dict__).dict(by_alias=False) for book in cheap_books
    ]
    return result


#
@history_routes.get(
    "/history/search",
    status_code=status.HTTP_200_OK,
    response_model=HistoryOut | list[HistoryOut],
    response_description="Search book history successfully",
)
async def get_history_for_book(
        request: Request,
        current_user: Annotated[UserResponse, Depends(verify_user)],
        book_id: Annotated[int, Query(title="Search book for id in db", qe=1)] = None,
        book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
        title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
        author: Annotated[str, Query(title="Search book for author", min_length=3)] = None,
):
    searcher = HistorySearchFacadeServices(
        search_history_service=RepositorySearchHistoryService(request.state.db),
        book_price_alert=RepositoryBookPriceAlertService(request.state.db)
    )

    books_history = await searcher.search_history(book_id, book_num, title, author)
    return [HistoryOut.parse_obj(books.__dict__) for books in books_history]
