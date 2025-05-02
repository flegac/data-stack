import shutil
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import JSONResponse

app = FastAPI()

# Répertoire pour stocker les fichiers téléchargés
UPLOAD_DIRECTORY = Path("uploads")
UPLOAD_DIRECTORY.mkdir(parents=True, exist_ok=True)


@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Vérifier le type de fichier (optionnel)
    allowed_extensions = {".jpg", ".jpeg", ".png", ".pdf"}
    file_extension = Path(file.filename).suffix.lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(status_code=400, detail="File type not allowed")

    # Chemin complet pour enregistrer le fichier
    file_location = UPLOAD_DIRECTORY / file.filename

    # Enregistrer le fichier
    with file_location.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return JSONResponse(
        content={"message": f"File {file.filename} uploaded successfully"}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, port=8000)
