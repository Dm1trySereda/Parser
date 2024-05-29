from typing import Annotated

from fastapi import APIRouter, HTTPException, Query, status
from starlette.requests import Request

from src.repository.history import RepetitiveBook
from src.response_schemas.history import HistoryOut
from src.services.search_history_services.repository import (
    AbstractSearchHistoryService,
    RepositorySearchHistoryService,
)

history_routes = APIRouter(tags=["History"])

#
# @history_routes.get(
#     "/history/search",
#     status_code=status.HTTP_200_OK,
#     response_model=HistoryOut | list[HistoryOut],
#     response_description="Search book history successfully",
# )
# async def get_history_book(
#     request: Request,
#     book_id: Annotated[int, Query(title="Search book for id in db", qe=1)] = None,
#     book_num: Annotated[int, Query(title="Search book for num", qe=100)] = None,
#     title: Annotated[str, Query(title="Search book for title", min_length=3)] = None,
#     author: Annotated[str, Query(title="Search book for author", min_length=3)] = None,
# ):
#     searcher: AbstractSearchHistoryService = RepositorySearchHistoryService(
#         request.state.db
#     )
#     try:
#         validate_parameters(
#             book_id=book_id, bok_num=book_num, title=title, author=author
#         )
#     except AttributeError as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=str(e),
#         )
#     books_history = await searcher.search(
#         book_id=book_id, book_num=book_num, title=title, author=author
#     )
#     try:
#         validate_searcher(search_book=books_history)
#     except ValueError as e:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
#     return (
#         [HistoryOut.parse_obj(books.__dict__) for books in books_history]
#         if isinstance(books_history, list)
#         else HistoryOut.parse_obj(books_history.__dict__)
#     )


@history_routes.get(
    "/history/repetitive/",
    status_code=status.HTTP_200_OK,
    response_model=list[HistoryOut],
    response_description="History successfully",
)
async def get_repetitive_books(request: Request):
    book_repetitive = RepetitiveBook(request.state.db)
    repetitive = await book_repetitive.select_all_history()
    result = [
        HistoryOut.parse_obj(book.__dict__).dict(by_alias=False) for book in repetitive
    ]
    return result
