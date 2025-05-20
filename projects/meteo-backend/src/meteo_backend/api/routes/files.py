import numpy as np
from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import Response
from meteo_domain.core.logger import logger
from meteo_domain.datafile_ingestion.entities.workspace import Workspace
from scipy.interpolate import griddata

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.dependencies import get_context

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


@router.post("/heatmap")
async def get_heatmap(
    points: list[list[float]], values: list[float], width: int = 512, height: int = 512
):
    points = np.array(points)
    values = np.array(values)

    buffer = generate_heatmap(points, values, width, height)

    return Response(content=buffer.getvalue(), media_type="image/png")


def generate_heatmap(points, values, width, height):
    # Créer une grille pour l'interpolation
    grid_x, grid_y = np.mgrid[0 : 1 : width * 1j, 0 : 1 : height * 1j]

    # Interpoler les données
    interpolated_values = griddata(
        points, values, (grid_x, grid_y), method="nearest", fill_value=0.0
    )

    # Normaliser les valeurs interpolées pour qu'elles soient entre 0 et 255
    interpolated_values_normalized = (
        (interpolated_values - interpolated_values.min())
        / (interpolated_values.max() - interpolated_values.min())
        * 255
    )
    interpolated_values_normalized = interpolated_values_normalized.astype(np.uint8)

    # Créer une figure et afficher la heatmap
    fig, ax = plt.subplots()
    ax.imshow(interpolated_values_normalized, cmap="viridis", extent=[0, 1, 0, 1])
    ax.scatter(points[:, 0], points[:, 1], c="red", s=10)
    ax.set_title("Heatmap des Points 2D")

    # Sauvegarder la figure dans un buffer
    buffer = BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)

    return buffer
