import asyncio

from meteo_app.wires.config import INI_FILE
from meteo_app.wires.services import Services
from meteo_app.workers.data_file_ingestion_listener import DataFileIngestionListener


def main():
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())
    services.wire(modules=[__name__])

    worker = DataFileIngestionListener()
    asyncio.run(worker.run())


if __name__ == "__main__":
    main()
