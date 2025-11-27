from dataclasses import dataclass, field
from typing import final

from travelexhibition.core.events import ArtifactCreatedEvent
from travelexhibition.ports.broker_ports import MessageBrokerPublisherProtocol
from travelexhibition.setup.config import BrokerConfig


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateArtifactHandler:
    broker: MessageBrokerPublisherProtocol
    topic: str = field(default=BrokerConfig.broker_new_artifact_queue)

    async def __call__(self, event: ArtifactCreatedEvent) -> None:
        await self.broker.publish_event(key=str(event.aggregate_id), topic=self.topic, event=event)