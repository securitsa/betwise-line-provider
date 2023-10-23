from domain.entities.event import Event, EventStatus
from ports.repositories.event_repository import EventRepository


class SaveEventUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def __call__(self, event: Event) -> Event:
        event.status = EventStatus.SCHEDULED
        event = await self.event_repository.save(event)
        return event
