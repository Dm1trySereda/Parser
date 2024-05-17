# === Базовый образ ===
FROM python:3.10 as base
WORKDIR /myapp
COPY .env /myapp
COPY pyproject.toml /myapp
RUN pip install poetry && POETRY_VIRTUALENVS_CREATE=false poetry install

# === Сборка с celery ===
FROM base as celery-stage
COPY src/ /myapp/src
COPY celery_run.sh /myapp
RUN chmod +x /myapp/celery_run.sh
CMD ["sh", "/myapp/celery_run.sh"]

# === Сборка с fastapi ===
FROM base as fastapi-stage
COPY celery_run.sh /myapp
CMD  [ "uvicorn", "src.services.parser.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]