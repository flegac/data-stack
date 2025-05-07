import logging

from aa_common.repo.repository import Repository


async def check_repository[Entity](
    repo: Repository[Entity],
    item: Entity,
):
    logging.getLogger("asyncio").setLevel(logging.ERROR)

    await repo.init()

    async def log_all():
        async for _ in repo.find_all():
            print(_)
        print("-------------------")

    uid = await repo.create_or_update(item)
    await log_all()

    await repo.delete_by_id(uid)
    await log_all()

    await repo.create_or_update(item)
    await log_all()
