from advanced_alchemy.extensions.litestar import SQLAlchemyPlugin
from litestar import Litestar, get

from travelexhibition.adapters.secondary.database.sessions import get_sqlalchemy_config
from travelexhibition.config import PostgresConfig


@get("/")
async def index() -> str:
    return "Hello, world!"


db_config = PostgresConfig()
app = Litestar(
    route_handlers=[index],
    plugins=[SQLAlchemyPlugin(config=get_sqlalchemy_config(db_config))],
)
