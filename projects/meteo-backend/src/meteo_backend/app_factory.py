from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from meteo_backend.api.routes import health, files
from meteo_backend.core.config.container import Container
from meteo_backend.core.config.settings import Settings


def create_app(container: Container | None = None) -> tuple[FastAPI, Settings]:
    app = FastAPI(title="Meteo Backend API")

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Configure container
    if container is None:
        container = Container()
        container.settings.override(Settings())

    # Wire container
    container.wire(
        modules=[
            "meteo_backend.api.routes.files",
            "meteo_backend.api.routes.health",
        ]
    )

    # Include routers
    app.include_router(health.router, prefix="/api/v1", tags=["health"])
    app.include_router(files.router, prefix="/api/v1/files", tags=["files"])

    return app, container.settings()
