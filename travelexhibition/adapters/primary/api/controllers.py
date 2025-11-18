from uuid import UUID
from typing import Annotated

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, route, HttpMethod, Response
from litestar.params import Parameter
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE

from travelexhibition.adapters.primary.api.errors import log_error
from travelexhibition.adapters.primary.api.schemas import ArtifactResponseSchema
from travelexhibition.adapters.secondary.exceptions import SQLAlchemyReaderError, DataMapperError
from travelexhibition.core.dtos import GetArtifactDTO
from travelexhibition.core.models import Artifact
from travelexhibition.core.services import GetArtifactInteractor


class ArtifactController(Controller):
    path = "/artifact"

    @route(
        http_method=HttpMethod.GET,
        path="/{artifact_id:uuid}",
        return_dto=ArtifactResponseSchema,
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
                status_code=HTTP_503_SERVICE_UNAVAILABLE,
            ),
        },
        default_error_handler=log_error,
        status_code=HTTP_200_OK,
    )
    @inject
    async def get_artifact(
            self,
            artifact_id: Annotated[UUID, Parameter(description="Artifact ID", title="Artifact ID")],
            interactor: Depends[GetArtifactInteractor],
    ) -> Artifact:
        return await interactor(GetArtifactDTO(artifact_id=artifact_id))
