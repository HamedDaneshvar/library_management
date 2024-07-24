from celery import Celery
from celery.schedules import crontab

from app.core.config import settings


BROKER_URL = f"amqp://{settings.RABBITMQ_USERNAME}:{settings.RABBITMQ_PASSWORD}@{settings.RABBITMQ_HOST}:{settings.RABBITMQ_PORT}"
print(f"---------{BROKER_URL}-----")
celery_app = Celery("worker", backend="rpc://", broker=BROKER_URL)

celery_app.conf.task_routes = {"app.celery.worker.test_celery": "main-queue"}
celery_app.conf.update(task_track_started=True)


celery_app.conf.update(
    beat_schedule={
        "deduct_book_cost-for-daily": {
            "task": "app.celery.tasks.deduct_book_cost",
            "schedule": crontab(hour="*/24")

        }
    },
)

celery_app.autodiscover_tasks(["app.celery"])
