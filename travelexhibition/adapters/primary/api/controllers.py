from uuid import UUID
from typing import Annotated

from dishka.integrations.base import FromDishka as Depends
from dishka.integrations.litestar import inject
from litestar import Controller, route, HttpMethod, Response
from litestar.params import Parameter, Body
from litestar.status_codes import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_503_SERVICE_UNAVAILABLE, HTTP_201_CREATED

from travelexhibition.adapters.primary.api.errors import log_error
from travelexhibition.adapters.primary.api.schemas import ArtifactResponseSchema, ArtifactCreateResponseSchema, \
    ArtifactCreateRequestSchema
from travelexhibition.adapters.secondary.exceptions import SQLAlchemyReaderError, DataMapperError
from travelexhibition.core.dtos import GetArtifactDTO, CreateArtifactDTO
from travelexhibition.core.models import Artifact
from travelexhibition.core.services import GetArtifactInteractor, CreateArtifactInteractor


class ArtifactController(Controller):
    path = "/artifacts"

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

    @route(
        http_method=HttpMethod.POST,
        path="/",
        dto=ArtifactCreateRequestSchema,
        return_dto=ArtifactCreateResponseSchema,
        summary="Create Artifact",
        description="Creates a new artifact in the database and send to kafka",
        name="artifact:create",
        tags=["Artifacts"],
        exception_handlers={
            SQLAlchemyReaderError: lambda request, exc: Response(
                content={"error": "Bad request", "detail": str(exc)},
                status_code=HTTP_400_BAD_REQUEST,
            ),
        },
        default_error_handler=log_error,
        status_code=HTTP_201_CREATED,
    )
    @inject
    async def create_artifact(
            self,
            data: Annotated[Artifact, Body(title="Create Artifact", description="Create a new artifact.")],
            interactor: Depends[CreateArtifactInteractor],
    ) -> Artifact:
        return await interactor(
            CreateArtifactDTO(
                title=data.title,
                model3d_url=data.model3d_url,
                description=data.description
            )
        )



