import asyncio
from celery import group, chain
from .core import parser_app
from database.repository import update_or_insert_books_sync, insert_books_history_sync
from async_parser import reading_session


@parser_app.task(name="reading_pages_sync")
def reading_pages_sync(page: int) -> list:
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(reading_session(page))


@parser_app.task(name="insert_books_task")
def insert_books_task(pages: list):
    return update_or_insert_books_sync(pages)


@parser_app.task(name="write_history_to_db")
def insert_books_history_task():
    return insert_books_history_sync()


def run_tasks():
    read_tasks = group(reading_pages_sync.s(i) for i in range(1, 101))
    write_tasks_chain = chain(read_tasks, insert_books_task.s())
    result = write_tasks_chain.delay()
    result.get()
    insert_books_history_task.delay()


if __name__ == "__main__":
    run_tasks()
