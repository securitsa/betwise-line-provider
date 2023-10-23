from fastapi import Depends

from routers.dependencies.repositories import get_event_repository
from usecases.events.list_events_use_case import ListEventsUseCase
from usecases.events.save_event_use_case import SaveEventUseCase


def get_save_event_use_case(event_repository=Depends(get_event_repository)):
    return SaveEventUseCase(event_repository)


def get_list_events_use_case(event_repository=Depends(get_event_repository)):
    return ListEventsUseCase(event_repository)
