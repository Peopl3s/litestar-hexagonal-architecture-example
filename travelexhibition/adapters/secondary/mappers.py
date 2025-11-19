from typing import final

from orjson import orjson

from travelexhibition.core.events import DomainEvent


@final
class OrjsonEventSerializer:
    @staticmethod
    def serialize(event: DomainEvent) -> bytes:
        return orjson.dumps(event)