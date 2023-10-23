from pydantic import BaseModel, Field

from routers.v1.event.schema import EventItem


class EventsCollection(BaseModel):
    total_count: int = Field(ge=0)
    items: list[EventItem]
    links: dict
