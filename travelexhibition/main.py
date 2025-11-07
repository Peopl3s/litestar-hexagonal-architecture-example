from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin
from dishka import make_async_container
from dishka.integrations.litestar import setup_dishka, LitestarProvider
from litestar import Litestar, get
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig

from travelexhibition.adapters.primary.api.controllers import ArtifactController
from travelexhibition.adapters.secondary.database.sessions import get_sqlalchemy_config
from travelexhibition.config import PostgresConfig
from travelexhibition.ioc import AppProvider

logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",  # Включить логирование исключений с трассировкой
)

db_config = PostgresConfig()

container = make_async_container(LitestarProvider(), AppProvider())

app = Litestar(
    route_handlers=[ArtifactController],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0", path="/api"),
    plugins=[SQLAlchemyInitPlugin(config=get_sqlalchemy_config(db_config))],
    logging_config=logging_config,
)

setup_dishka(container, app)
