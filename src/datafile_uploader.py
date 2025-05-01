import asyncio

from wires.application import ApplicationContainer
from worker.data_file_upload_worker import DataFileUploadWorker

if __name__ == '__main__':
    container = ApplicationContainer()
    container.check_dependencies()
    container.wire(modules=[__name__])

    worker = DataFileUploadWorker()

    asyncio.run(worker.run())
