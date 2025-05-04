from datetime import datetime, UTC

from dependency_injector.wiring import inject
from fastapi import APIRouter, Depends

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.dependencies import get_context

router = APIRouter()


@router.get("/health")
@inject
async def health_check(
    context: ApplicationContext = Depends(get_context),
):
    return {
        "status": "healthy",
        "version": context.settings.VERSION,
        "timestamp": datetime.now(UTC).isoformat(),
    }
