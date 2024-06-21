import asyncio
from datetime import datetime, timezone
from parser.async_parser import reading_session

from celery import chain, group
from celery.schedules import crontab
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from celery_worker.config.celery_configs import parser
from src.config.database.db_helpers import db_helper
from src.request_shemas.parser_book import ParserBook
from src.services.create_new_book_service.repository import RepositoryAddNewBookService
from src.services.delete_inactive_user_service.repository import (
    RepositoryDeleteInactiveUserService,
)
from src.services.parser_facade import ParserHandler
from src.services.search_book_service.repository import RepositorySearchBookService
from src.services.update_book_service.repository import RepositoryUpdateBookService
from src.services.update_history_service.repository import (
    RepositoryUpdateHistoryService,
)

parser.conf.timezone = "Europe/Moscow"
parser.conf.beat_schedule = {
    "run-every-10-minutes": {
        "task": "add_books_group",
        "schedule": crontab(minute="*/2"),
    }
}


@parser.task(name="reading_pages")
def reading_pages(page: int) -> list:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(reading_session(page))


@parser.task(name="create_or_update_books")
def create_or_update_books(pages: list) -> None:
    loop = asyncio.get_event_loop()

    async def wrapped():
        async with db_helper.get_db_session() as async_session:
            books_handler = ParserHandler(
                search_services=RepositorySearchBookService(async_session),
                update_services=RepositoryUpdateBookService(async_session),
                insert_services=RepositoryAddNewBookService(async_session),
                update_history_services=RepositoryUpdateHistoryService(async_session),
            )
            for books in pages:
                if not books:
                    continue
                for book in books:
                    try:
                        valid_book = ParserBook.parse_obj(book)
                    except ValidationError:
                        continue
                    try:
                        await books_handler.process_books(valid_book)
                        await async_session.commit()
                    except IntegrityError:
                        await async_session.rollback()

    return loop.run_until_complete(wrapped())


@parser.task(name="add_books_history")
def add_books_history() -> None:
    loop = asyncio.get_event_loop()

    async def wrapper():
        async with db_helper.get_db_session() as async_session:
            book_handler = ParserHandler(
                search_services=RepositorySearchBookService(async_session),
                update_services=RepositoryUpdateBookService(async_session),
                insert_services=RepositoryAddNewBookService(async_session),
                update_history_services=RepositoryUpdateHistoryService(async_session),
            )

            await book_handler.process_books_history()

    return loop.run_until_complete(wrapper())


@parser.task(name="delete_inactive_user")
def delete_inactive_user() -> None:
    loop = asyncio.get_event_loop()

    async def wrapper():
        async with db_helper.get_db_session() as async_session:
            current_time = datetime.now(timezone.utc)
            user_handler = RepositoryDeleteInactiveUserService(async_session)
            await user_handler.delete_inactive_user(current_time)

    return loop.run_until_complete(wrapper())


current_range_start = 1


@parser.task(name="add_books_group")
def add_books_group():
    global current_range_start
    read_tasks = group(
        reading_pages.s(i)
        for i in range(current_range_start, current_range_start + 100)
    )
    write_tasks_chain = chain(
        read_tasks, create_or_update_books.s(), add_books_history.si()
    )
    write_tasks_chain.delay()
    delete_inactive_user.delay()
    current_range_start += 100
    if current_range_start > 800:
        current_range_start = 1
