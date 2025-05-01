import asyncio

from wires.application import ApplicationContainer
from worker.measure_ingestion_listener import MeasureIngestionListener

if __name__ == '__main__':
    container = ApplicationContainer()
    container.check_dependencies()
    container.wire(modules=[__name__])

    worker = MeasureIngestionListener(
        topic='temperature'
    )

    asyncio.run(worker.run())
