from litestar.plugins.sqlalchemy import repository

from travelexhibition.adapters.secondary.database.models import Artifact as ArtifactModel
from travelexhibition.core.models import Artifact as ArtifactDM
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort


class UsersRepositoryAdapter(
    ArtifactRepositoryPort, repository.SQLAlchemyAsyncRepository[ArtifactModel]
):
    model_type = ArtifactModel

    async def get_by_id(self, artifact_id: str) -> ArtifactDM:
        artifact_model = await self.get_one(id=artifact_id)
        return ArtifactDM(
            id=artifact_model.id,
            title=artifact_model.title,
            model3d_url=artifact_model.model3d_url,
            description=artifact_model.description,
        )
