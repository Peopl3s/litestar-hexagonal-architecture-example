from dataclasses import dataclass
from uuid import UUID
from datetime import datetime
from enum import Enum


class EventType(Enum):
    CREATED = "created"
    UPDATED = "updated"
    DELETED = "deleted"


@dataclass(frozen=True, slots=True, kw_only=True)
class BaseDomainEvent:
    event_type: EventType
    occurred_at: datetime
    aggregate_id: UUID
    aggregate_type: str = "artifact"


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactCreatedEvent(BaseDomainEvent):
    event_type: str = EventType.CREATED.value
    title: str
    model3d_url: str
    description: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactUpdatedEvent(BaseDomainEvent):
    event_type: str = EventType.UPDATED.value
    title: str
    model3d_url: str
    description: str | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ArtifactDeletedEvent(BaseDomainEvent):
    event_type: str = EventType.DELETED.value


DomainEvent = ArtifactCreatedEvent | ArtifactUpdatedEvent | ArtifactDeletedEvent
