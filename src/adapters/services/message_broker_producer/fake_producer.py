from core.exceptions.external_exceptions import MessageProducerException
from ports.services.message_broker_producer import MessageBrokerProducer


class FakeProducer(MessageBrokerProducer):
    with_error = False

    async def send_message(self, queue_name: str, payload: dict) -> None:
        if self.with_error:
            raise MessageProducerException
