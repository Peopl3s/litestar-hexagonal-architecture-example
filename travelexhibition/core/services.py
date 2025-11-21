from dataclasses import dataclass
from datetime import datetime
from typing import final

from travelexhibition.core.dtos import GetArtifactDTO, CreateArtifactDTO
from travelexhibition.core.events import ArtifactCreatedEvent
from travelexhibition.core.models import Artifact as ArtifactDM, ArtifactID
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort
from travelexhibition.ports.event_bus import EventBusPort


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactInteractor:
    artifact_gateway: ArtifactRepositoryPort

    async def __call__(self, request_data: GetArtifactDTO) -> ArtifactDM:
        artifact_id = ArtifactID(value=request_data.artifact_id)
        return await self.artifact_gateway.get_by_id(artifact_id)


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class CreateArtifactInteractor:
    artifact_gateway: ArtifactRepositoryPort
    event_bus: EventBusPort

    async def __call__(self, request_data: CreateArtifactDTO) -> ArtifactDM:
        artifact = await self.artifact_gateway.create_one(request_data)
        artifact_event = ArtifactCreatedEvent(
            title=request_data.title,
            model3d_url=request_data.model3d_url,
            description=request_data.description,
            aggregate_id=artifact.id.value,
            occurred_at=datetime.utcnow(),
        )
        await self.event_bus.publish(artifact_event)
        return artifact