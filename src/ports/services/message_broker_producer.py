from abc import ABC, abstractmethod


class MessageBrokerProducer(ABC):
    @abstractmethod
    async def send_message(self, queue_name: str, payload: dict) -> None:
        pass
