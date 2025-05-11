from functools import cached_property
from pathlib import Path

from aa_common.logger import logger
from aa_common.mq.mq_backend import MQBackend
from meteo_domain.config import (
    DATAFILE_INGESTION_TOPIC,
    DATAFILE_ERROR_TOPIC,
    MEASURE_TOPIC,
)
from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle
from meteo_domain.entities.workspace import Workspace
from meteo_domain.ports.data_file_repository import DataFileRepository
from meteo_domain.ports.file_repository import FileRepository
from meteo_domain.ports.measure_repository import MeasureRepository
from posix_measure_repository.data_file_measure_repository import (
    DataFileMeasureRepository,
)


class DataFileService:

    def __init__(
        self,
        data_file_repository: DataFileRepository,
        file_repository: FileRepository,
        measure_repository: MeasureRepository,
        mq_backend: MQBackend,
    ):
        self.data_file_repository = data_file_repository
        self.file_repository = file_repository
        self.mq_backend = mq_backend
        self.measure_repository = measure_repository

    async def update_status(self, item: DataFile, status: DataFileLifecycle):
        item.status = status
        await self.data_file_repository.create_or_update(item)

    async def start_ingest_listener(self):
        await self.ingestion_consumer.listen(self.ingest_file)

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
            await self.error_handler(item, e)
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
            await self.ingestion_producer.write_single(item)
            return item
        except Exception as e:
            await self.error_handler(item, e)
            raise e

    @cached_property
    def ingestion_producer(self):
        return self.mq_backend.producer(DATAFILE_INGESTION_TOPIC)

    @cached_property
    def ingestion_consumer(self):
        return self.mq_backend.consumer(DATAFILE_INGESTION_TOPIC)

    @cached_property
    def error_producer(self):
        return self.mq_backend.producer(DATAFILE_ERROR_TOPIC)

    @cached_property
    def measure_producer(self):
        return self.mq_backend.producer(MEASURE_TOPIC)

    async def error_handler(self, item: DataFile, error: Exception = None):
        logger.warning(f"_handle_error: {error}: {item}")
        item.status = DataFileLifecycle.ingestion_failed
        await self.data_file_repository.create_or_update(item)
        await self.error_producer.write_single(item)
