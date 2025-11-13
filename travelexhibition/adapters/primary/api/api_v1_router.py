from litestar import Router

from travelexhibition.adapters.primary.api.controllers import ArtifactController


def create_api_v1_router() -> Router:
    router = Router(
        path="/api/v1",
        route_handlers=[ArtifactController]
    )
    return router