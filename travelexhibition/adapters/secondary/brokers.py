import logging
from dataclasses import dataclass
from typing import final

from faststream.kafka import KafkaBroker
from faststream.exceptions import FastStreamException

from travelexhibition.adapters.secondary.exceptions import BrokerPublishError
from travelexhibition.adapters.secondary.mappers import OrjsonEventSerializer
from travelexhibition.core.events import DomainEvent
from travelexhibition.ports.broker_ports import MessageBrokerPublisherProtocol

log = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class KafkaPublisher(MessageBrokerPublisherProtocol):
    broker: KafkaBroker
    serializer: OrjsonEventSerializer

    async def publish_event(self, key: str, topic: str, event: DomainEvent) -> None:
        try:
            await self.broker.publish(
                key=key,
                message=self.serializer.serialize(event=event),
                topic=topic,
            )
        except FastStreamException as e:
            log.error("Failed to publish", exc_info=e)
            raise BrokerPublishError from e