from abc import ABC, abstractmethod

from domain.entities.event import Event


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
