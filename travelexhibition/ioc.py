from litestar import Request
from sqlalchemy.ext.asyncio import AsyncSession
from dishka import Provider, provide, Scope

from travelexhibition.adapters.secondary.database.repositories import ArtifactRepositoryAdapter
from travelexhibition.core.services import GetArtifactUseCase
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort


class AppProvider(Provider):
    @provide(scope=Scope.REQUEST)
    async def get_async_session(self, request: Request) -> AsyncSession:
        return request.state.sqlalchemy_session

    @provide(scope=Scope.REQUEST)
    def artifact_repo(self, session: AsyncSession) -> ArtifactRepositoryPort:
        return ArtifactRepositoryAdapter(session=session)

    get_artifact_use_case = provide(GetArtifactUseCase, scope=Scope.REQUEST)