import asyncio

import uvicorn

from meteo_backend.core.app_factory import create_app
from meteo_backend.core.config.container import Container

container = Container()
settings = container.settings()
app = create_app(container)


if __name__ == "__main__":
    asyncio.run(container.data_file_repository().init())

    module_path = f"{__name__}:app"
    uvicorn.run(
        module_path,
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        workers=1,
    )
