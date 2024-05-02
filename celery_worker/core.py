import os
from celery import Celery
from dotenv import load_dotenv

load_dotenv()

parser_app = Celery(
    'core',
    broker=os.getenv('BROKER_URL'),
    backend=os.getenv('RESULT_BACKEND'),
    include=['celery_worker.tasks'],

)
