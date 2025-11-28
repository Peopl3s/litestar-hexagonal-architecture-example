from litestar.dto import DataclassDTO, DTOConfig

from travelexhibition.core.models import Artifact


class ArtifactResponseSchema(DataclassDTO[Artifact]):
    config = DTOConfig()


class ArtifactCreateResponseSchema(DataclassDTO[Artifact]):
    config = DTOConfig(include={"id"})

class ArtifactCreateRequestSchema(DataclassDTO[Artifact]):
    config = DTOConfig(exclude={"id"})