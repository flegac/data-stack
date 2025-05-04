from fastapi import APIRouter, UploadFile, Depends

from aa_common.logger import logger
from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.dependencies import get_context

router = APIRouter()


@router.post("/upload")
async def upload_file(
    file: UploadFile,
    context: ApplicationContext = Depends(get_context),
):
    filepath = context.settings.LOCAL_STORAGE_PATH / "uploads" / file.filename
    filepath.parent.mkdir(parents=True, exist_ok=True)
    logger.info(f'filename: "{file.filename}"\npath: "{filepath}"')
    with filepath.open("wb") as f:
        content = await file.read()
        f.write(content)
    return await context.file_service.upload_single(filepath)
