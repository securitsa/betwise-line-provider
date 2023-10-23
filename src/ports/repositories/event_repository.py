from abc import ABC, abstractmethod
from typing import Unpack

from domain.entities.event import Event
from usecases.enum_models import EventFilters, EventSorting, Ordering


class EventRepository(ABC):
    @abstractmethod
    async def save(self, event: Event) -> Event:
        pass

    @abstractmethod
    async def find_by_token(self, token: str) -> Event:
        pass

    @abstractmethod
    async def exists(self, token: str) -> bool:
        pass

    @abstractmethod
    async def list(
        self,
        page: int = 1,
        limit: int = 50,
        sort_by: EventSorting = EventSorting.BY_CREATION_DATE,
        order_by: Ordering = Ordering.ASC,
        **filters: Unpack[EventFilters],
    ) -> list[Event]:
        pass

    @abstractmethod
    async def count(self, **filters: Unpack[EventFilters]) -> int:
        pass
