# demo_celery_standalone.py
import multiprocessing
import os
import subprocess
import time


def start_worker():
    os.environ["PYTHONPATH"] = os.getcwd()
    subprocess.run(
        ["celery", "-A", "demo_celery", "worker", "--loglevel=INFO"], check=False
    )


if __name__ == "__main__":
    # Démarrage du worker dans un processus séparé
    worker_process = multiprocessing.Process(target=start_worker)
    worker_process.start()

    # Attendre que le worker soit prêt
    print("Démarrage du worker Celery...")
    time.sleep(5)

    try:
        # Importer et exécuter la démo
        from demo_celery import run_demo

        run_demo()
    finally:
        # Nettoyage
        worker_process.terminate()
        worker_process.join()
