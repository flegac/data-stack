from pathlib import Path

from aa_common.logger import logger
from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.ports.measure_repository import MeasureRepository
from meteo_domain.services.datafile_messaging_service import (
    DataFileMessagingService,
)
from posix_measure_repository.data_file_measure_repository import (
    DataFileMeasureRepository,
)


class DataFileService:
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

    async def update_status(self, item: DataFile, status: DataFileLifecycle):
        item.status = status
        await self.data_file_repository.create_or_update(item)

    async def start_ingest_listener(self):
        await self.messaging.ingestion_consumer.listen(self.ingest_file)

    async def ingest_file(self, item: DataFile):
        logger.info(f"{item}")

        try:
            assert item.status in [DataFileLifecycle.upload_completed]
            await self.update_status(item, DataFileLifecycle.ingestion_in_progress)
            item.local_path = await self.file_repository.download_file(item.uid)
            source_repository = DataFileMeasureRepository(item)

            def measure_provider():
                for measures in source_repository.search():
                    for measure in measures:
                        yield measure

            try:
                await self.measure_repository.save_batch(
                    measures=measure_provider(),
                    chunk_size=200_000,
                )
                await self.update_status(item, DataFileLifecycle.ingestion_completed)
            except Exception:
                await self.update_status(item, DataFileLifecycle.ingestion_failed)
                raise

            return item
        except Exception as e:
            await self.messaging.error_handler(item, e)
            raise

    async def upload_single(self, ws: Workspace, path: Path) -> DataFile | None:
        item = DataFile.from_file(path)
        item.workspace_id = ws.uid
        logger.info(item)

        if existing := await self.data_file_repository.find_by_id(item.uid):
            logger.warning(f'"{item.uid}" already exists:\n{existing}')
        if existing := self.data_file_repository.find_all(
            source_hash=item.source_hash,
        ):
            logger.warning(
                f'source_hash "{item.source_hash}" already exists:\n'
                f"{[_.uid async for _ in existing]}"
            )

        await self.data_file_repository.create_or_update(item)

        try:
            await self.update_status(item, DataFileLifecycle.upload_in_progress)
            await self.file_repository.upload_file(
                item.uid, item.local_path.read_bytes()
            )
            await self.update_status(item, DataFileLifecycle.upload_completed)
            await self.messaging.ingestion_producer.write_single(item)
            return item
        except Exception as e:
            await self.messaging.error_handler(item, e)
            raise e
