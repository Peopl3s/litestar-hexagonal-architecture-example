from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactDTO:
    artifact_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateArtifactDTO:
    title: str
    model3d_url: str
    description: str | None = None