from datetime import datetime, timedelta
from uuid import UUID

from pydantic import BaseModel

from domain.entities.event import Event, EventStatus


class EventInput(BaseModel):
    name: str
    description: str
    coefficient: float
    timeline: timedelta

    def to_entity(self, administrator_token: str) -> Event:
        return Event(
            administrator_token=administrator_token,
            name=self.name,
            description=self.description,
            coefficient=self.coefficient,
            expiration_at=datetime.now() + self.timedelta,
        )


class EventItem(BaseModel):
    token: UUID
    administrator_token: str
    name: str
    description: str | None
    coefficient: float
    expiration_at: datetime
    status: EventStatus
    created_at: datetime
    status_updated_at: datetime | None

    @classmethod
    def from_entity(cls, event: Event):
        return cls(
            token=event.token,
            administrator_token=event.administrator_token,
            name=event.name,
            coefficient=event.coefficient,
            status=event.status,
            created_at=event.created_at,
            description=event.description,
            status_updated_at=event.status_updated_at,
        )
