from celery import Celery
from pydantic_settings import BaseSettings


class ConfigCelery(BaseSettings):
    BROKER_URL: str
    RESULT_BACKEND: str
    INCLUDE: list = ["src.celery_worker.tasks"]

    class Config:
        extra = "ignore"


config_celery = ConfigCelery()

parser = Celery(
    "celery_configs",
    broker=config_celery.BROKER_URL,
    backend=config_celery.RESULT_BACKEND,
    include=config_celery.INCLUDE,
)


