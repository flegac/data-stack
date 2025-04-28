import asyncio
from pathlib import Path

from data_file_ingestion.data_file import DataFile
from data_file_repository_pg.pg_data_file_repository import PgDataFileRepository


async def main():
    repository = PgDataFileRepository(
        database_url="postgresql+asyncpg://admin:adminpassword@localhost:5432/mydatabase"
    )
    await repository.init()

    datafile = DataFile.from_file(
        path=Path(__file__).absolute()
    )
    await repository.create_or_update(datafile)

    async for datafile in repository.read_all():
        print(datafile)

    # Suppression d'un DataFile
    await repository.delete("http://example.com/12345")

    await repository.close()


if __name__ == '__main__':
    asyncio.run(main())
