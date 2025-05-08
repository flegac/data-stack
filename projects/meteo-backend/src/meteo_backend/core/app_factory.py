from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from meteo_backend.api.routes import files, health
from meteo_backend.core.config.container import Container


def create_app(container: Container) -> FastAPI:
    app = FastAPI(title="Meteo Backend API")
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

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

    return app
