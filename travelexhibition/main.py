from advanced_alchemy.extensions.litestar import SQLAlchemyInitPlugin
from litestar import Litestar, get
from litestar.logging import LoggingConfig
from litestar.openapi import OpenAPIConfig

from travelexhibition.adapters.secondary.database.sessions import get_sqlalchemy_config
from travelexhibition.config import PostgresConfig


@get("/")
async def index() -> str:
    return "Hello, world!"

logging_config = LoggingConfig(
    root={"level": "INFO", "handlers": ["queue_listener"]},
    formatters={
        "standard": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}
    },
    log_exceptions="always",  # Включить логирование исключений с трассировкой
)

db_config = PostgresConfig()

app = Litestar(
    route_handlers=[index],
    openapi_config=OpenAPIConfig(title="My API", version="1.0.0"),
    plugins=[SQLAlchemyInitPlugin(config=get_sqlalchemy_config(db_config))],
    logging_config=logging_config,
)
