import logging

from meteo_domain.core.repository import Repository


async def check_repository[Entity](
    repo: Repository[Entity],
    item: Entity,
):
    logging.getLogger("asyncio").setLevel(logging.ERROR)

    async def log_all():
        async for _ in repo.find_all():
            print(_)
        print("-------------------")

    uid = await repo.save(item)
    await log_all()

    await repo.delete_by_id(uid)
    await log_all()

    await repo.save(item)
    await log_all()
