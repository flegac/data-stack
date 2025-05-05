import uvicorn

from meteo_backend.app_factory import create_app

app, settings = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "meteo_backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        workers=1,
    )
