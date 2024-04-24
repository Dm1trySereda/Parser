FROM python:3.10
WORKDIR /myapp
COPY requirements.txt /myapp
RUN pip install -r requirements.txt
COPY celery_main.py /myapp
CMD ["celery", "-A", "celery_main", "worker", "-l", "INFO"]
#ENTRYPOINT ["python", "celery_main.py"]

#docker exec -it id_container python celery_main.py - запустит выполнение скрипта