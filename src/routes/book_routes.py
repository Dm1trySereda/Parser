from typing import Annotated

from fastapi import APIRouter, Body, Depends, Query, status
from starlette.requests import Request

from src.enums.book import SortChoices
from src.enums.role import UserRoleEnum
from src.models.users import User
from src.request_shemas.books import BookIn
from src.response_schemas.books import BookOuts
from src.services.add_new_book_facade import AddNewBookFacade
from src.services.add_new_book_service.repository import RepositoryAddNewBookService
from src.services.authorization_facade import AuthorizationFacade
from src.services.delete_book_faсade import DeleteBookFacade
from src.services.delete_book_service.repository import RepositoryDeleteBookService
from src.services.paginate_facade import PaginationFacade
from src.services.paginate_service.repository import RepositoryPaginateBookService
from src.services.search_book_facade import BookSearchFacadeServices
from src.services.search_book_service.repository import RepositorySearchBookService
from src.services.update_book_facade import UpdateBookFacade
from src.services.update_book_service.repository import RepositoryUpdateBookService
from src.services.update_history_service.repository import (
    RepositoryUpdateHistoryService,
)
from src.services.validate_token_service.repository import (
    RepositoryValidateTokenService,
)

book_router = APIRouter(tags=["Books"])
auth_facade = AuthorizationFacade(
    validate_token_service_service=RepositoryValidateTokenService()
)


@book_router.get(
    "/books/search",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
)
async def search_books(
    request: Request,
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin, UserRoleEnum.client]
        )
    ),
    book_id: Annotated[
        int, Query(alias="id", title="Search book for id in db", qe=1)
    ] = None,
    book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
    title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
    author: Annotated[str, Query(title="Search book for author", min_length=3)] = None,
):
    searcher = BookSearchFacadeServices(
        search_book_service=RepositorySearchBookService(request.state.db)
    )
    search_result = await searcher.search_book(book_id, book_num, title, author)
    return [BookOuts.parse_obj(books.__dict__) for books in search_result]


@book_router.get(
    "/books/",
    status_code=status.HTTP_200_OK,
    response_description="Search successful",
    response_model=list[BookOuts],
)
async def get_books_on_page(
    request: Request,
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin, UserRoleEnum.client]
        )
    ),
    page: Annotated[int, Query(qe=1)] = 1,
    books_quantity: Annotated[int, Query(qe=10)] = None,
    sort_by: Annotated[SortChoices, Query()] = SortChoices.title,
    order_asc: Annotated[bool, Query()] = False,
) -> list[BookOuts]:
    paginator = PaginationFacade(
        pagination_services=RepositoryPaginateBookService(request.state.db)
    )
    page = await paginator.paginate(page, books_quantity, sort_by, order_asc)

    return [BookOuts.parse_obj(books.__dict__) for books in page]


@book_router.post(
    "/books/create",
    status_code=status.HTTP_201_CREATED,
    response_model=BookOuts,
    response_description="Book added",
)
async def add_book(
    request: Request,
    new_book: Annotated[BookIn, Body(embed=False)],
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin]
        )
    ),
):
    book_inserter = AddNewBookFacade(
        search_services=RepositorySearchBookService(request.state.db),
        inserter_services=RepositoryAddNewBookService(request.state.db),
        history_updater_services=RepositoryUpdateHistoryService(request.state.db),
    )
    new_book = await book_inserter.add_new_book(new_book)
    return new_book


@book_router.put(
    "/books/edit",
    status_code=status.HTTP_200_OK,
    response_model=BookOuts,
    response_description="Book updated",
)
async def change_book(
    request: Request,
    book: Annotated[BookIn, Body(embed=False)],
    user: User = Depends(
        auth_facade.get_permissions_checker(
            roles=[UserRoleEnum.admin, UserRoleEnum.subadmin]
        )
    ),
):
    book_updater = UpdateBookFacade(
        searcher_services=RepositorySearchBookService(request.state.db),
        updater_services=RepositoryUpdateBookService(request.state.db),
        history_updater_services=RepositoryUpdateHistoryService(request.state.db),
    )
    updated_book = await book_updater.update_book(book)
    return updated_book


@book_router.delete(
    "/books/remove",
    status_code=status.HTTP_202_ACCEPTED,
    response_description="Book deleted",
    response_model=BookOuts,
)
async def delete_book(
    request: Request,
    book_id: Annotated[int, Query(qe=1)] = None,
    book_num: Annotated[int, Query(qe=100)] = None,
    user: User = Depends(
        auth_facade.get_permissions_checker(roles=[UserRoleEnum.admin])
    ),
):
    book_deleter = DeleteBookFacade(
        search_services=RepositorySearchBookService(request.state.db),
        delete_services=RepositoryDeleteBookService(request.state.db),
    )
    book = await book_deleter.delete_book(book_id, book_num)
    return book
