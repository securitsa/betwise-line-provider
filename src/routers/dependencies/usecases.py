from fastapi import Depends

from core.config import get_settings
from routers.dependencies.repositories import get_event_repository
from routers.dependencies.services import get_message_broker_producer
from usecases.events.list_events_use_case import ListEventsUseCase
from usecases.events.save_event_use_case import SaveEventUseCase
from usecases.events.update_event_status_use_case import UpdateEventUseCase


def get_save_event_use_case(event_repository=Depends(get_event_repository)):
    return SaveEventUseCase(event_repository)


def get_list_events_use_case(event_repository=Depends(get_event_repository)):
    return ListEventsUseCase(event_repository)


def get_update_event_use_case(
    settings=Depends(get_settings),
    event_repository=Depends(get_event_repository),
    message_broker_producer=Depends(get_message_broker_producer),
):
    return UpdateEventUseCase(settings, event_repository, message_broker_producer)
