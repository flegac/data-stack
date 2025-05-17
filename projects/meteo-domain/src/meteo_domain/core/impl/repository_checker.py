from meteo_domain.datafile_ingestion.ports.uow.repository import Repository
from meteo_domain.datafile_ingestion.ports.uow.unit_of_work import UnitOfWork


async def check_uow_repository[Entity](
    uow: UnitOfWork,
    repo: Repository[Entity],
    item: Entity,
):
    # async with uow.transaction():
    #     await repo.drop_table()

    async with uow.transaction():
        await repo.create_table()

    async with uow.transaction():
        await repo.save(item)
        await log_all(repo)

    async with uow.transaction():
        await repo.delete_by_id(item.uid)
        await log_all(repo)

    async with uow.transaction():
        await repo.save(item)
        await log_all(repo)


async def log_all(repo: Repository):
    print(f"--- content of {str(repo):30s} ----------------")
    async for _ in repo.find_all():
        print(_)
    print("--------------------------------------------------------------")
