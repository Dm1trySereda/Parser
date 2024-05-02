FROM python:3.10
WORKDIR /myapp
COPY requirements.txt /myapp
RUN pip install -r requirements.txt
COPY . /myapp
CMD ["celery", "-A", "celery_worker.core", "worker", "-l", "INFO"]