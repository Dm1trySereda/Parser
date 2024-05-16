#!/bin/sh
celery -A src.config.celery_configs worker -l info &
celery -A src.services.celery.tasks beat -l info