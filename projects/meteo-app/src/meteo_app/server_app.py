import shutil
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

# Répertoire pour stocker les fichiers téléchargés
UPLOAD_DIRECTORY = Path("uploads")


@app.post("/upload/")
async def upload_file(file: UploadFile):
    allowed_extensions = {".grib", ".h5"}
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400, detail=f"File type not allowed: {file.filename}"
        )

    file_location = UPLOAD_DIRECTORY / file.filename
    UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(
        content={"message": f"File {file.filename} uploaded successfully"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
