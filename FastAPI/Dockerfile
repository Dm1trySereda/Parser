FROM python:3.10
WORKDIR /myapp
COPY ../requirements.txt /myapp
RUN pip install -r requirements.txt
COPY ../FastAPI /myapp/FastAPI
COPY ../database /myapp/database
COPY ../.env /myapp/
CMD  [ "uvicorn", "FastAPI.parser_api:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]