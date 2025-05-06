# demo_celery.py
import logging
import random
import time
from datetime import datetime

from celery import Celery

THRESHOLD = 0.5

# Configuration du logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Création de l'application Celery
app = Celery(
    "tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0",
)


# Configuration
app.conf.update(
    task_track_started=True,
    task_time_limit=30,
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
)


# Simulation d'une API externe
def mock_api_call(duration=None):
    if duration is None:
        duration = random.uniform(0.5, 2)
    time.sleep(duration)
    return {"status": "success", "timestamp": datetime.now().isoformat()}


# Tâches Celery
@app.task(bind=True, name="tasks.simple_task")
def simple_task(self, name):
    logger.info(f"Executing simple task for {name}")
    result = mock_api_call(1)
    return f"Hello {name} at {result['timestamp']}"


@app.task(bind=True, name="tasks.error_prone_task")
def error_prone_task(self, should_fail=False):
    if should_fail:
        raise ValueError("Task failed as requested")
    if random.random() < THRESHOLD:
        raise Exception("Random failure!")
    result = mock_api_call()
    return result


@app.task(bind=True, name="tasks.long_task")
def long_task(self, duration):
    logger.info(f"Starting long task for {duration} seconds")
    mock_api_call(duration)
    return f"Completed long task after {duration} seconds"


def run_demo():
    logger.info("Starting Celery demo...")

    # 1. Tâche simple
    logger.info("1. Lancement d'une tâche simple")
    result = simple_task.delay("Alice")
    logger.info(f"Tâche simple lancée avec ID: {result.id}")
    logger.info(f"Résultat: {result.get()}")

    # 2. Tâche avec erreur
    logger.info("\n2. Lancement d'une tâche avec erreur")
    result = error_prone_task.delay(should_fail=True)
    try:
        result.get()
    except Exception as e:
        logger.error(f"Erreur attendue: {str(e)}")

    # 3. Plusieurs tâches en parallèle
    logger.info("\n3. Lancement de plusieurs tâches en parallèle")
    tasks = []
    for i in range(3):
        task = simple_task.delay(f"User{i}")
        tasks.append(task)

    # Attente des résultats
    for i, task in enumerate(tasks):
        logger.info(f"Résultat tâche {i}: {task.get()}")

    # 4. Tâche longue avec timeout
    logger.info("\n4. Lancement d'une tâche longue")
    result = long_task.delay(3)
    try:
        # Attente du résultat avec timeout
        result.get(timeout=5)
        logger.info("Tâche longue terminée avec succès")
    except Exception as e:
        logger.error(f"Erreur ou timeout: {str(e)}")

    logger.info("\nDémo terminée!")


if __name__ == "__main__":
    # Pour exécuter ce script, vous devez avoir:
    # 1. Redis en cours d'exécution
    # 2. Un worker Celery démarré dans un autre terminal avec:
    #    celery -A demo_celery worker --loglevel=INFO

    print(
        """
    Avant de lancer ce script, assurez-vous que:
    1. Redis est en cours d'exécution (redis-server)
    2. Lancez le worker Celery dans un autre terminal avec:
       celery -A demo_celery worker --loglevel=INFO
    
    Appuyez sur Enter pour continuer...
    """
    )
    input()

    run_demo()
