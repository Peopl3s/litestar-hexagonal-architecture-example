from abc import abstractmethod
from typing import Protocol

from travelexhibition.core.models import Artifact, ArtifactID


class ArtifactRepositoryPort(Protocol):
    @abstractmethod
    async def get_by_id(self, artifact_id: ArtifactID) -> Artifact: ...
