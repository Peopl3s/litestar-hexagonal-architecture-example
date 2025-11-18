from dataclasses import dataclass
from typing import final

from travelexhibition.core.dtos import GetArtifactDTO
from travelexhibition.core.models import Artifact as ArtifactDM, ArtifactID
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort


@final
@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactInteractor:
    artifact_gateway: ArtifactRepositoryPort

    async def __call__(self, request_data: GetArtifactDTO) -> ArtifactDM:
        artifact_id = ArtifactID(value=request_data.artifact_id)
        return await self.artifact_gateway.get_by_id(artifact_id)
