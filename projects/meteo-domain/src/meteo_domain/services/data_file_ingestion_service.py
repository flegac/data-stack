from aa_common.logger import logger
from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.entities.measurement.measurement import Measurement
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.ports.measure_repository import MeasureRepository
from meteo_domain.services.data_file_messaging_service import (
    DataFileMessagingService,
)
from posix_measure_repository.data_file_measure_repository import (
    DataFileMeasureRepository,
)

BATCH_SIZE = 10_000


class DataFileIngestionService:
    def __init__(
        self,
        messaging: DataFileMessagingService,
        data_file_repository: DataFileRepository,
        file_repository: FileRepository,
        measure_repository: MeasureRepository,
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.messaging = messaging
        self.measure_repository = measure_repository

    async def ingestion_listener(self):
        await self.messaging.ingestion_consumer.listen(self.ingest_file)

    async def ingest_file(self, item: DataFile):
        logger.info(f"{item}")

        try:
            assert item.status in [DataFileLifecycle.upload_completed]

            await self.data_file_repository.update_status(
                item, DataFileLifecycle.ingestion_in_progress
            )

            item.local_path = await self.file_repository.download_file(item.uid)

            source_repository = DataFileMeasureRepository(item)
            provider = source_repository.search()

            try:
                batch: list[Measurement] = []
                for measures in provider:
                    batch.extend(measures)
                    if len(batch) >= BATCH_SIZE:
                        await self.measure_repository.save_batch(batch)
                        batch.clear()
                    # await self.messaging.measure_producer.write_batch(measures)
                await self.measure_repository.save_batch(batch)
                await self.data_file_repository.update_status(
                    item, DataFileLifecycle.ingestion_completed
                )
            except Exception:
                await self.data_file_repository.update_status(
                    item, DataFileLifecycle.ingestion_failed
                )
                raise

            return item
        except Exception as e:
            await self.messaging.error_handler(item, e)
            raise
