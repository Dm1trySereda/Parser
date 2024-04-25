FROM python:3.10
WORKDIR /myapp
COPY requirements.txt /myapp
RUN pip install -r requirements.txt
COPY celery_main.py /myapp
COPY test_api.py /myapp
CMD ["celery", "-A", "celery_main", "worker", "-l", "INFO"]