from uuid import UUID
from typing import Annotated

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, route, HttpMethod
from litestar.params import Parameter

from travelexhibition.adapters.primary.api.schemas import ArtifactResponseSchema
from travelexhibition.core.services import GetArtifactUseCase


class ArtifactController(Controller):
    path = "/artifact"

    @route(http_method=HttpMethod.GET, path="/{artifact_id:uuid}", response_model=ArtifactResponseSchema)
    @inject
    async def get_artifact(
            self,
            artifact_id: Annotated[UUID, Parameter(description="Artifact ID", title="Artifact ID")],
            use_case: Depends[GetArtifactUseCase],
    ) -> ArtifactResponseSchema:
        artifact_dm = await use_case(str(artifact_id))
        return ArtifactResponseSchema(
            id=artifact_dm.id,
            title=artifact_dm.title,
            description=artifact_dm.description,
            model3d_url=artifact_dm.model3d_url
        )
