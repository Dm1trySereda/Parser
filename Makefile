run-task-in-docker:
	docker exec parser python celery_worker/celery_tasks.py