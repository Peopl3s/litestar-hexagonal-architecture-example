from dataclasses import dataclass
from typing import final

from travelexhibition.core.models import Artifact as ArtifactDM
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactUseCase:
    artifact_gateway: ArtifactRepositoryPort

    async def __call__(self, artifact_id: str) -> ArtifactDM:
        return await self.artifact_gateway.get_by_id(artifact_id)
