from pathlib import Path
from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch

from fastapi.testclient import TestClient

from meteo_backend.core.application_context import ApplicationContext
from meteo_backend.core.config.settings import Settings
from meteo_backend.main import create_app
from meteo_domain.entities.data_file import DataFile
from meteo_domain.entities.datafile_lifecycle import DataFileLifecycle


class TestFilesAPI(IsolatedAsyncioTestCase):
    def setUp(self):
        # Créer les mocks pour les services
        self.mock_file_service = AsyncMock()
        self.mock_ingestion_service = AsyncMock()
        self.mock_messaging_service = AsyncMock()

        # Créer un Settings avec un chemin temporaire de test
        self.test_settings = Settings(LOCAL_STORAGE_PATH=Path("/tmp/test-meteo-files"))

        # Créer un ApplicationContext mock
        self.mock_context = ApplicationContext(
            settings=self.test_settings,
            file_service=self.mock_file_service,
            ingestion_service=self.mock_ingestion_service,
            messaging_service=self.mock_messaging_service,
        )

        # Créer une nouvelle instance de l'application pour les tests
        self.app = create_app()

        # Patcher get_context avant de créer le TestClient
        self.context_patcher = patch(
            "meteo_backend.core.dependencies.get_context",
            return_value=self.mock_context,
        )

        # Démarrer le patch avant tout
        self.context_patcher.start()

        # Créer le client de test après le patch
        self.client = TestClient(self.app)
        self.headers = {"X-API-Key": "your-api-key-here"}

    def tearDown(self):
        # Arrêter le patch
        self.context_patcher.stop()
        # Nettoyer les fichiers temporaires si nécessaire
        if self.test_settings.LOCAL_STORAGE_PATH.exists():
            import shutil

            shutil.rmtree(self.test_settings.LOCAL_STORAGE_PATH)

    async def test_upload_file(self):
        # Préparer un fichier de test
        test_content = b"test file content"
        test_filename = "test_file.nc"

        # Créer un DataFile de test pour le retour du service
        test_data_file = DataFile(
            data_id=test_filename,
            source_hash="abc123",
            source_uri=str(
                self.test_settings.LOCAL_STORAGE_PATH / "uploads" / test_filename
            ),
            status=DataFileLifecycle.upload_completed,
        )

        # Configurer le mock du service pour retourner le DataFile de test
        self.mock_file_service.upload_single.return_value = test_data_file

        # Simuler l'upload de fichier
        response = self.client.post(
            "/api/v1/files/upload",
            files={"file": (test_filename, test_content)},
            headers=self.headers,
        )

        # Vérifier la réponse
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["data_id"], test_filename)
        self.assertEqual(DataFileLifecycle[data["status"]], test_data_file.status)

        # Vérifier que le service mocké a été appelé correctement
        self.mock_file_service.upload_single.assert_called_once()
        call_args = self.mock_file_service.upload_single.call_args[0][0]
        self.assertEqual(
            call_args, self.test_settings.LOCAL_STORAGE_PATH / "uploads" / test_filename
        )
