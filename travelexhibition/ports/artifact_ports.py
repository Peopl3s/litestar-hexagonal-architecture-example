from abc import abstractmethod
from typing import Protocol

from travelexhibition.core.dtos import CreateArtifactDTO
from travelexhibition.core.models import Artifact, ArtifactID


class ArtifactRepositoryPort(Protocol):
    @abstractmethod
    async def get_by_id(self, artifact_id: ArtifactID) -> Artifact: ...

    @abstractmethod
    async def create_one(self, data: CreateArtifactDTO) -> Artifact: ...
