import asyncio
from parser.async_parser import reading_session
from celery import chain, group
from celery.schedules import crontab

from celery_worker.config.celery_configs import parser
from src.repository.parser_handler.books import BaseHandler, DeleteDuplicateHandler

parser.conf.timezone = "Europe/Moscow"
parser.conf.beat_schedule = {
    "run-every-10-minutes": {
        "task": "add_books_group",
        "schedule": crontab(minute="*/10"),
    }
}

current_range_start = 1


@parser.task(name="reading_pages")
def reading_pages(page: int) -> list:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(reading_session(page))


@parser.task(name="delete_duplicates")
def delete_duplicates():
    book_handler = DeleteDuplicateHandler()
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(book_handler.remove_duplicates())


@parser.task(name="insert_books")
def insert_books(pages: list) -> None:
    loop = asyncio.get_event_loop()
    books = BaseHandler()
    return loop.run_until_complete(books.process_books(pages))


@parser.task(name="add_books_history")
def add_books_history() -> None:
    loop = asyncio.get_event_loop()
    books_history = BaseHandler()
    return loop.run_until_complete(books_history.process_books_history())


@parser.task(name="add_books_group")
def add_books_group():
    global current_range_start
    delete_duplicates.delay()
    read_tasks = group(
        reading_pages.s(i) for i in range(current_range_start, current_range_start + 50)
    )
    write_tasks_chain = chain(read_tasks, insert_books.s(), add_books_history.si())
    write_tasks_chain.delay()
    current_range_start += 50
    if current_range_start > 350:
        current_range_start = 1
