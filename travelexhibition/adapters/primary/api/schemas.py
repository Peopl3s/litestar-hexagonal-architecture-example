from litestar.dto import DataclassDTO, DTOConfig

from travelexhibition.core.models import Artifact


class ArtifactResponseSchema(DataclassDTO[Artifact]):
    config = DTOConfig()