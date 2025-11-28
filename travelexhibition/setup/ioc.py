import logging
from collections.abc import AsyncIterator, Iterable

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine, async_sessionmaker
from dishka import Provider, provide, Scope, from_context

from travelexhibition.adapters.secondary.brokers import KafkaPublisher
from travelexhibition.adapters.secondary.database.event_handlers import CreateArtifactHandler
from travelexhibition.adapters.secondary.database.repositories import ArtifactRepositoryAdapter
from travelexhibition.adapters.secondary.database.uow import SqlAlchemyUnitOfWork
from travelexhibition.adapters.secondary.event_bus import EventBusAdapter
from travelexhibition.core.events import EventType
from travelexhibition.ports.broker_ports import MessageBrokerPublisherProtocol
from travelexhibition.ports.event_bus import EventBusPort
from travelexhibition.ports.uow_ports import UnitOfWork
from travelexhibition.setup.config import PostgresConfig, SqlEngineConfig, AppConfig
from travelexhibition.core.services import GetArtifactInteractor, CreateArtifactInteractor
from travelexhibition.setup.logging import LoggingConfig
from travelexhibition.ports.artifact_ports import ArtifactRepositoryPort

log = logging.getLogger(__name__)


class SettingsProvider(Provider):
    scope = Scope.APP

    settings = from_context(AppConfig)

    @provide
    def postgres_config(self, settings: AppConfig) -> PostgresConfig:
        return settings.postgres_config

    @provide
    def sql_engine_config(self, settings: AppConfig) -> SqlEngineConfig:
        return settings.sql_engine_config

    @provide
    def logging_config(self, settings: AppConfig) -> LoggingConfig:
        return settings.logging_config


class ApplicationProvider(Provider):
    scope = Scope.REQUEST

    @provide
    def get_artifact_interactor(self, repository: ArtifactRepositoryPort) -> GetArtifactInteractor:
        return GetArtifactInteractor(artifact_gateway=repository)

    @provide
    def get_create_artifact_interactor(
            self,
            repository: ArtifactRepositoryPort,
            event_bus: EventBusPort
    ) -> CreateArtifactInteractor:
        return CreateArtifactInteractor(artifact_gateway=repository, event_bus=event_bus)

    @provide
    def get_artifact_repository(self, session: AsyncSession) -> ArtifactRepositoryPort:
        return ArtifactRepositoryAdapter(session=session)

    @provide
    def get_event_bus(self) -> EventBusPort:
        event_bus = EventBusAdapter()
        event_bus.subscribe(event_type=EventType.CREATED, handler=CreateArtifactHandler)
        return event_bus

    @provide
    def get_create_artifact_handler(self, broker: MessageBrokerPublisherProtocol) -> CreateArtifactHandler:
        return CreateArtifactHandler(broker=broker)

    tx_manager = provide(SqlAlchemyUnitOfWork, provides=UnitOfWork)

    broker = provide(KafkaPublisher, provides=MessageBrokerPublisherProtocol)


class PersistenceSqlProvider(Provider):
    @provide(scope=Scope.APP)
    async def provide_async_engine(
        self,
        postgres_config: PostgresConfig,
        sql_engine_config: SqlEngineConfig,
    ) -> AsyncIterator[AsyncEngine]:
        async_engine = create_async_engine(
            url=str(postgres_config.database_url),
            echo=sql_engine_config.echo,
            echo_pool=sql_engine_config.echo_pool,
            pool_size=sql_engine_config.pool_size,
            max_overflow=sql_engine_config.max_overflow,
            connect_args={"command_timeout": 5},
            pool_pre_ping=True,
        )
        log.debug("Async engine created with DSN: %s", postgres_config.database_url)
        yield async_engine
        log.debug("Disposing async engine...")
        await async_engine.dispose()
        log.debug("Engine is disposed.")

    @provide(scope=Scope.APP)
    def provide_async_session_factory(
        self,
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        async_session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            expire_on_commit=False,
        )
        log.debug("Async session maker initialized.")
        return async_session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_async_session(
        self,
        async_session_factory: async_sessionmaker[AsyncSession],
    ) -> AsyncIterator[AsyncSession]:
        log.debug("Starting async session...")
        async with async_session_factory() as session:
            log.debug("Async session started.")
            yield session
            log.debug("Closing async session.")
        log.debug("Async session closed.")


def get_providers() -> Iterable[Provider]:
    return (
        SettingsProvider(),
        ApplicationProvider(),
        PersistenceSqlProvider(),
    )
