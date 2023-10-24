from core.settings import BaseAppSettings
from domain.entities.event import Event, EventStatus
from ports.repositories.event_repository import EventRepository
from ports.services.message_broker_producer import MessageBrokerProducer


class UpdateEventUseCase:
    def __init__(
        self, settings: BaseAppSettings, event_repository: EventRepository, message_producer: MessageBrokerProducer
    ):
        self.settings = settings
        self.event_repository = event_repository
        self.message_producer = message_producer

    async def __call__(self, token: str, status: EventStatus) -> Event:
        event = await self.event_repository.find_by_token(token)
        payload = {"token": token, "status": status}
        await self.message_producer.send_message(self.settings.events_queue, payload)
        event.status = status
        event = await self.event_repository.save(event)
        return event
