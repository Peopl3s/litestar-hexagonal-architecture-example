from abc import abstractmethod
from collections.abc import Callable
from typing import Protocol

from travelexhibition.core.events import BaseDomainEvent, EventType


class EventBusPort(Protocol):
    @abstractmethod
    def subscribe(self, event_type: EventType, handler: Callable) -> None: ...

    @abstractmethod
    async def publish(self, event: BaseDomainEvent) -> None: ...