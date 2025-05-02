import asyncio

from wires.config import INI_FILE
from wires.services import Services
from worker.data_file_ingestion_listener import DataFileIngestionListener

if __name__ == "__main__":
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())

    services.wire(modules=[__name__])

    worker = DataFileIngestionListener()

    asyncio.run(worker.run())
