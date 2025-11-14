from uuid import UUID
from typing import Annotated

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, route, HttpMethod, Response
from litestar.params import Parameter
from litestar.status_codes import HTTP_400_BAD_REQUEST

from travelexhibition.adapters.primary.api.schemas import ArtifactResponseSchema
from travelexhibition.adapters.secondary.exceptions import SQLAlchemyReaderError, DataMapperError
from travelexhibition.core.dtos import GetArtifactDTO
from travelexhibition.core.services import GetArtifactUseCase


class ArtifactController(Controller):
    path = "/artifact"

    @route(
        http_method=HttpMethod.GET,
        path="/{artifact_id:uuid}",
        response_model=ArtifactResponseSchema,
        summary="Get Artifact by ID",
        description="Fetches a specific artifact using its unique identifier (UUID).",
        name="artifact:get_by_id",
        tags=["Artifacts"],
        exception_handlers={
            SQLAlchemyReaderError: lambda request, exc: Response(
                content={"error": "Bad request", "detail": str(exc)},
                status_code=HTTP_400_BAD_REQUEST,
            ),
            DataMapperError: lambda request, exc: Response(
                content={"error": "Bad request", "detail": str(exc)},
                status_code=HTTP_400_BAD_REQUEST,
            ),
        }
    )
    @inject
    async def get_artifact(
            self,
            artifact_id: Annotated[UUID, Parameter(description="Artifact ID", title="Artifact ID")],
            use_case: Depends[GetArtifactUseCase],
    ) -> ArtifactResponseSchema:
        artifact_dm = await use_case(GetArtifactDTO(artifact_id=artifact_id))
        return ArtifactResponseSchema(
            id=artifact_dm.id.value,
            title=artifact_dm.title,
            description=artifact_dm.description,
            model3d_url=artifact_dm.model3d_url
        )
