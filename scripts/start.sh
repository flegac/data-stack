#!/bin/bash

# Répertoire contenant les fichiers Docker Compose
COMPOSE_DIR=docker-starter

# Vérifier si le répertoire existe
if [ ! -d "$COMPOSE_DIR" ]; then
    echo "Directory $COMPOSE_DIR does not exist."
    exit 1
fi

# Parcourir le répertoire et lancer chaque fichier Docker Compose
for compose_file in "$COMPOSE_DIR"/*.yml "$COMPOSE_DIR"/*.yaml; do
    if [ -f "$compose_file" ]; then
        echo "Starting services from $compose_file..."
        docker-compose -f "$compose_file" up -d
    fi
done

echo "All Docker Compose services have been started."
