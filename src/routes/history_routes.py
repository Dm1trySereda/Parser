from typing import Annotated

from fastapi import APIRouter, Depends, Query, status, HTTPException
from starlette.requests import Request

from src.custom_exceptions.exseptions import (
    ResultError,
    ProvidingParametersError,
    BookHistoryError,
)
from src.enums.history import HistorySortChoices
from src.enums.role import UserRoleEnum
from src.models.users import User
from src.response_schemas.history import HistoryOut
from src.services.authorization_facade import AuthorizationFacade
from src.services.book_price_alert_service.repository import (
    RepositoryBookPriceAlertService,
)
from src.services.search_history_faсade import HistorySearchFacadeServices
from src.services.search_history_service.repository import (
    RepositorySearchHistoryService,
)
from src.services.validate_token_service.repository import (
    RepositoryValidateTokenService,
)

history_routes = APIRouter(tags=["History"])
auth_facade = AuthorizationFacade(
    validate_token_service_service=RepositoryValidateTokenService()
)


@history_routes.get(
    "/history/",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="History successfully",
)
async def show_history(
    request: Request,
    page: Annotated[int, Query(qe=1)] = 1,
    books_quantity: Annotated[int, Query(qe=10)] = None,
    sort_by: Annotated[HistorySortChoices, Query()] = HistorySortChoices.title,
    order_asc: Annotated[bool, Query()] = False,
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin]
        )
    ),
):
    searcher = HistorySearchFacadeServices(
        search_history_service=RepositorySearchHistoryService(request.state.db),
        book_price_alert=RepositoryBookPriceAlertService(request.state.db),
    )
    try:
        cheap_books = await searcher.get_cheap_books(
            page, books_quantity, sort_by, order_asc
        )
    except ResultError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return cheap_books


#
@history_routes.get(
    "/history/search",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="Search book history successfully",
)
async def get_history_for_book(
    request: Request,
    book_id: Annotated[int, Query(title="Search book for id in db", qe=1)] = None,
    book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
    title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
    author: Annotated[str, Query(title="Search book for author", min_length=3)] = None,
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin, UserRoleEnum.client]
        )
    ),
):
    searcher = HistorySearchFacadeServices(
        search_history_service=RepositorySearchHistoryService(request.state.db),
        book_price_alert=RepositoryBookPriceAlertService(request.state.db),
    )
    try:

        books_history = await searcher.search_history(book_id, book_num, title, author)
    except ProvidingParametersError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    except BookHistoryError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
    return books_history
