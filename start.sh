#!/bin/sh
celery -A src.config.celery_configs worker -l info &
celery -A src.celery_worker.tasks beat -l info