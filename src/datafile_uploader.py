import asyncio

from wires.services import Services
from worker.data_file_upload_worker import DataFileUploadWorker

if __name__ == "__main__":
    container = Services()
    container.check_dependencies()
    container.wire(modules=[__name__])

    worker = DataFileUploadWorker()

    asyncio.run(worker.run())
