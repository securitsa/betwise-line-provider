from fastapi import Depends

from routers.dependencies.repositories import get_event_repository
from usecases.events.save_event_use_case import SaveEventUseCase


def get_save_event_use_case(event_repository=Depends(get_event_repository)):
    return SaveEventUseCase(event_repository)
