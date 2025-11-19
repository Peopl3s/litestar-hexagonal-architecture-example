from abc import abstractmethod
from typing import Protocol

from travelexhibition.core.events import DomainEvent


class MessageBrokerPublisherProtocol(Protocol):
    @abstractmethod
    async def publish_event(self, key: str, topic: str, event: DomainEvent) -> None: ...
