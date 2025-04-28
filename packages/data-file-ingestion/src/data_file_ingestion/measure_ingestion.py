from data_file_ingestion.data_file import DataFile
from data_file_ingestion.data_file_repository import DataFileRepository


class MeasureIngestionService:
    def __init__(self, data_file_repository: DataFileRepository):
        self.data_file_repository = data_file_repository

    async def register_file(self, item: DataFile):
        # 1. upload file to S3
        # TODO

        # 2. save metadata to DataFileRepository
        await self.data_file_repository.create_or_update(item)

        # 3. add to Queue "data_file_pending"
        # TODO
