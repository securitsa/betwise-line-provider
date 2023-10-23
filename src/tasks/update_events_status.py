import logging

from core.loggers import TASK_WORKER_LOGGER
from scheduler import celery_app

# from tasks.di_container import StatusWorkerContainer

# di_container = StatusWorkerContainer
logger = logging.getLogger(TASK_WORKER_LOGGER)


async def update_events_status() -> None:
    # async with di_container() as container:
    #     events = await container.event_repository.list()
    logger.info(1)


@celery_app.task(name="update_events_status", serializer="pickle")
def update_events_status() -> None:
    logger.info(1)
