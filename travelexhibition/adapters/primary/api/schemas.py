from uuid import UUID

from pydantic import BaseModel


class ArtifactResponseSchema(BaseModel):
    id: UUID
    title: str
    model3d_url: str
    description: str | None = None