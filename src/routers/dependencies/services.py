from aiobotocore.session import get_session
from fastapi import Depends

from adapters.services.message_broker_producer.sqs_producer import SQSProducer
from core.config import get_settings
from core.settings import BaseAppSettings
from ports.services.message_broker_producer import MessageBrokerProducer


def get_message_broker_producer(
    session=Depends(get_session), settings: BaseAppSettings = Depends(get_settings)
) -> MessageBrokerProducer:
    return SQSProducer(session, settings)
