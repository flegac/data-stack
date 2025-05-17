from fastapi import APIRouter, Depends, UploadFile

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.dependencies import get_context
from meteo_domain.core.logger import logger
from meteo_domain.workspace.entities.workspace import Workspace

router = APIRouter()


@router.post("/upload/{workspace_uid}")
async def upload_file(
    workspace_uid: str,
    file: UploadFile,
    context: ApplicationContext = Depends(get_context),  # noqa: B008
):
    async with context.uow.transaction():
        ws = await context.ws_service.ws_repository.find_by_id(workspace_uid)
        if not ws:
            ws = Workspace(uid=workspace_uid)
            await context.ws_service.ws_repository.save(ws)

    filepath = context.settings.LOCAL_STORAGE_PATH / "uploads" / file.filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f'filename: "{file.filename}"\npath: "{filepath}"')
    with filepath.open("wb") as f:
        content = await file.read()
        f.write(content)
    return await context.datafile_service.upload_single(ws, filepath)
