from litestar.plugins.sqlalchemy import repository
from sqlalchemy.exc import SQLAlchemyError

from travelexhibition.adapters.secondary.database.models import Artifact as ArtifactModel
from travelexhibition.adapters.secondary.exceptions import SQLAlchemyReaderError, DataMapperError
from travelexhibition.core.exceptions import DomainValidationError
from travelexhibition.core.models import Artifact as ArtifactDM, ArtifactID
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort


class ArtifactRepositoryAdapter(
    ArtifactRepositoryPort, repository.SQLAlchemyAsyncRepository[ArtifactModel]
):
    model_type = ArtifactModel

    async def get_by_id(self, artifact_id: ArtifactID) -> ArtifactDM:
        try:
            artifact_model = await self.get_one(id=artifact_id.value)
            return ArtifactDM(
                id=ArtifactID(value=artifact_model.id),
                title=artifact_model.title,
                model3d_url=artifact_model.model3d_url,
                description=artifact_model.description,
            )
        except SQLAlchemyError as err:
            raise SQLAlchemyReaderError("Database query failed.") from err
        except DomainValidationError as err:
            raise DataMapperError("Data mapping failed.") from err
