import os
from datetime import timedelta

from celery import Celery

from core.config import get_settings

settings = get_settings()
os.environ["C_FORCE_ROOT"] = "1"

celery_app = Celery(
    "celery_worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_backend_url,
)


celery_app.conf.update(
    task_track_started=True,
    task_serializer="pickle",
    result_serializer="pickle",
    accept_content=["pickle", "json"],
    result_expires=200,
    result_persistent=True,
    worker_send_task_events=False,
    worker_prefetch_multiplier=1,
)
celery_app.conf.beat_schedule = {
    "update-events-status": {
        "task": "update_events_status",
        "schedule": timedelta(seconds=10),
        "options": {"queue": "line_provider_queue"},
    }
}

celery_app.autodiscover_tasks(
    packages=[
        "tasks.update_events_status",
    ]
)
