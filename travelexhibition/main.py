from dishka import Provider
from dishka.integrations.litestar import setup_dishka

from litestar import Litestar

from travelexhibition.setup.app_factory import create_web_app, create_ioc_container
from travelexhibition.setup.config import AppConfig
from travelexhibition.setup.logging import configure_logging


def make_app(
    *di_providers: Provider,
    settings: AppConfig | None = None,
) -> Litestar:

    configure_logging()

    app: Litestar = create_web_app()
    container = create_ioc_container(settings, *di_providers)
    setup_dishka(container, app)

    return app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=make_app(),
        port=8000,
        reload=False,
        loop="uvloop",
    )
