# === Базовый образ ===
FROM python:3.10 as base
WORKDIR /myapp

RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE=false

COPY pyproject.toml /myapp
RUN poetry install
COPY src/ /myapp/src

# === Сборка с celery ===
FROM base as celery-stage
COPY celery_worker /myapp/celery_worker
COPY parser /myapp/parser
CMD ["celery", "-A", "celery_worker.config.celery_configs", "worker", "-l", "info", "-B"]

# === Сборка с fastapi ===
FROM base as fastapi-stage
COPY parser /myapp/parser
CMD  [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]