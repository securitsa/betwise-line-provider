from typing import Unpack

from domain.entities.event import Event
from ports.repositories.event_repository import EventRepository
from usecases.enum_models import EventFilters, EventSorting, Ordering


class ListEventsUseCase:
    def __init__(self, event_repository: EventRepository):
        self.event_repository = event_repository

    async def __call__(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: EventSorting = EventSorting.BY_CREATION_DATE.value,
        order_by: Ordering = Ordering.ASC.value,
        **filters: Unpack[EventFilters],
    ) -> (list[Event], int):
        events = await self.event_repository.list(page, limit, sort_by, order_by, **filters)
        count = await self.event_repository.count(**filters)
        return events, count
