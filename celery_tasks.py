from celery import group, chain
from parser import reading_pages
from db_worker import *
from celery_config import *

load_dotenv()


def main():
    create_tables.delay()
    read_tasks = group(reading_pages.s(i) for i in range(1, 20))
    read_tasks_chain = chain(read_tasks, write_to_db.s())
    library = read_tasks_chain.delay()
    library.get()
    write_history_to_db.delay()


if __name__ == '__main__':
    main()
