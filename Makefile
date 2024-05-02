run-task-in-docker:
	docker exec parser python celery_worker/tasks.py