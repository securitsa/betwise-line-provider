import json
import logging

from aiobotocore.session import AioSession

from core.exceptions.external_exceptions import MessageProducerException
from core.loggers import PRODUCER_LOGGER
from core.settings import BaseAppSettings, EnvironmentTypes
from ports.services.message_broker_producer import MessageBrokerProducer

logger = logging.getLogger(PRODUCER_LOGGER)


class SQSProducer(MessageBrokerProducer):
    def __init__(self, session: AioSession, settings: BaseAppSettings):
        self.session = session
        self.client_config = {"region_name": "eu-west-3"}
        if settings.environment == EnvironmentTypes.local:
            self.client_config.update(settings.test_sqs_config)
        self.attributes = {"senderService": {"StringValue": "User-management Service", "DataType": "String"}}

    async def send_message(self, queue_name: str, payload: dict) -> None:
        async with self.session.create_client("sqs", **self.client_config) as client:
            try:
                queue_url = (await client.get_queue_url(QueueName=queue_name))["QueueUrl"]
                await client.send_message(
                    QueueUrl=queue_url, MessageBody=json.dumps(payload), MessageAttributes=self.attributes
                )
            except Exception as e:
                logger.exception(e)
                raise MessageProducerException
