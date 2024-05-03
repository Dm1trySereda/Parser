FROM python:3.10
WORKDIR /myapp
COPY ../requirements.txt /myapp
RUN pip install -r requirements.txt
COPY ../celery_worker /myapp/celery_worker
COPY ../database /myapp/database
COPY ../parser.py /myapp/
COPY ../.env /myapp/
CMD ["celery", "-A", "celery_worker.core", "worker", "-l", "INFO"]