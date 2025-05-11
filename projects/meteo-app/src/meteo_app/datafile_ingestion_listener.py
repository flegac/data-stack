import asyncio

from meteo_app.wires.config import INI_FILE
from meteo_app.wires.services import Services


def main():
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())
    services.wire(modules=[__name__])

    service = services.datafile_service()

    asyncio.run(service.start_ingest_listener())


if __name__ == "__main__":
    main()
