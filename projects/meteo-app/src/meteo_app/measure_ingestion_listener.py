import asyncio

from meteo_app.wires.services import Services
from meteo_app.workers.measure_ingestion_listener import MeasureIngestionListener

if __name__ == "__main__":
    container = Services()
    container.check_dependencies()
    container.wire(modules=[__name__])

    worker = MeasureIngestionListener(topic="temperature")

    asyncio.run(worker.run())
