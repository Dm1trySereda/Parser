import asyncio
from parser.async_parser import reading_session

from celery import chain, group
from celery.schedules import crontab
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from celery_worker.config.celery_configs import parser
from src.config.database.db_helpers import db_helper
from src.models.users import BaseRole
from src.request_shemas.parser_book import ParserBook
from src.services.add_new_book_service.repository import RepositoryAddNewBookService
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

current_range_start = 1


@parser.task(name="reading_pages")
def reading_pages(page: int) -> list:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(reading_session(page))


@parser.task(name="create_or_update_books")
def create_or_update_books(pages: list) -> None:
    loop = asyncio.get_event_loop()

    async def wrapped():
        async with db_helper.get_db_session() as session:
            books_handler = ParserHandler(
                search_services=RepositorySearchBookService(session),
                update_services=RepositoryUpdateBookService(session),
                insert_services=RepositoryAddNewBookService(session),
                update_history_services=RepositoryUpdateHistoryService(session),
            )
            for books in pages:
                if not pages:
                    raise ValueError("Page not found")
                for book in books:
                    try:
                        valid_book = ParserBook.parse_obj(book)
                    except ValidationError:
                        continue
                    try:
                        await books_handler.process_books(valid_book)
                        await session.commit()
                    except IntegrityError:
                        await session.rollback()

    return loop.run_until_complete(wrapped())


@parser.task(name="add_books_history")
def add_books_history() -> None:
    loop = asyncio.get_event_loop()

    async def wrapper():
        async with db_helper.get_db_session() as session:
            book_handler = ParserHandler(
                search_services=RepositorySearchBookService(session),
                update_services=RepositoryUpdateBookService(session),
                insert_services=RepositoryAddNewBookService(session),
                update_history_services=RepositoryUpdateHistoryService(session),
            )

            await book_handler.process_books_history()

    return loop.run_until_complete(wrapper())


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
    current_range_start += 100
    if current_range_start > 800:
        current_range_start = 1
