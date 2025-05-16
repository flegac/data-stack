@echo off
setlocal enabledelayedexpansion

:: Répertoire contenant les fichiers Docker Compose
set COMPOSE_DIR=docker-starter

:: Vérifier si le répertoire existe
if not exist "%COMPOSE_DIR%" (
    echo Directory %COMPOSE_DIR% does not exist.
    exit /b 1
)

:: Parcourir le répertoire et lancer chaque fichier Docker Compose
for %%F in ("%COMPOSE_DIR%\*.yml" "%COMPOSE_DIR%\*.yaml") do (
    if exist "%%F" (
        echo Starting services from %%F...
        docker-compose -f "%%F" up -d
    )
)

echo All Docker Compose services have been started.
