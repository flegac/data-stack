import os
from pathlib import Path

import cv2
import imageio


def create_gif(input_dir, output_path, duration=1000):
    """
    Crée un GIF à partir des images dans un répertoire.

    :param input_dir: Répertoire contenant les images.
    :param output_path: Chemin de sortie pour le GIF.
    :param duration: Durée de chaque image en millisecondes.
    """
    files = [
        f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))
    ]
    files.sort()

    # Lire les images avec OpenCV
    images = []
    for file in files:
        file_path = os.path.join(input_dir, file)
        try:
            img = cv2.imread(file_path)
            if img is not None:
                # Convertir l'image OpenCV en format RGB
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img)
        except Exception as e:
            print(f"Impossible d'ouvrir le fichier {file_path}: {e}")

    if not images:
        print("Aucune image valide trouvée dans le répertoire.")
        return

    # Sauvegarder les images sous forme de GIF
    imageio.mimsave(output_path, images, duration=duration / 1000)


if __name__ == "__main__":
    input_dir = Path.cwd() / "output"

    output_path = "heatmap.gif"

    create_gif(input_dir, output_path)
