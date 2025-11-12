from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from travelexhibition.adapters.primary.api.controllers import ArtifactController
from travelexhibition.setup.config import AppConfig

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from dishka import AsyncContainer, Provider, make_async_container

from travelexhibition.setup.ioc import get_providers


def create_ioc_container(
    settings: AppConfig,
    *di_providers: Provider,
) -> AsyncContainer:
    return make_async_container(
        *get_providers(),
        *di_providers,
        context={AppConfig: settings},
    )


def create_web_app() -> Litestar:
    app = Litestar(
        route_handlers=[ArtifactController],
        openapi_config=OpenAPIConfig(title="My API", version="1.0.0", path="/api"),
    )
    return app


@asynccontextmanager
async def lifespan(app: Litestar) -> AsyncIterator[None]:
    yield None
    # https://dishka.readthedocs.io/en/stable/integrations/fastapi.html
    await app.state.dishka_container.close()