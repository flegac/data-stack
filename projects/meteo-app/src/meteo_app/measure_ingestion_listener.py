import asyncio

from meteo_app.wires.config import INI_FILE
from meteo_app.wires.services import Services
from meteo_app.workers.measure_ingestion_listener import MeasureIngestionListener

if __name__ == "__main__":
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())
    services.wire(modules=[__name__])

    worker = MeasureIngestionListener(topic="temperature")

    asyncio.run(worker.run())
