from dependency_injector import containers
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from meteo_backend.api.routes import files, health


def create_app(container: containers.DeclarativeContainer) -> FastAPI:
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
