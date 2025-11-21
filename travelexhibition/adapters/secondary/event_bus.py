from collections.abc import Callable
from dataclasses import dataclass, field

from travelexhibition.core.events import EventType, BaseDomainEvent
from travelexhibition.ports.event_bus import EventBusPort


@dataclass(frozen=True, slots=True, kw_only=True)
class EventBusAdapter(EventBusPort):
    _handlers: dict[EventType, list[Callable]] = field(default_factory=dict)

    def subscribe(self, event_type: EventType, handler: Callable) -> None:
        if event_type not in self._handlers:
            self._handlers[event_type] = []
        self._handlers[event_type].append(handler)

    async def publish(self, event: BaseDomainEvent) -> None:
        event_type: str = event.event_type.value
        if event_type in self._handlers:
            for handler in self._handlers[event.event_type]:
                await handler(event)
