from domain.entities.event import Event, EventStatus
from ports.repositories.event_repository import EventRepository


class UpdateEventUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def __call__(self, event_token: str, status: EventStatus) -> Event:
        event = await self.event_repository.find_by_token(event_token)
        event.status = status
        event = await self.event_repository.save(event)
        return event
