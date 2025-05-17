from unittest import TestCase

from fastapi.testclient import TestClient

import meteo_domain.config
from meteo_backend.core.app_factory import create_app
from meteo_domain.datafile_ingestion.entities.datafile import DataFile
from meteo_domain.datafile_ingestion.entities.datafile_lifecycle import (
    DataFileLifecycle,
)
from mocked_container import MockedContainer


class TestFilesAPI(TestCase):
    def setUp(self):
        # Créer le container de test
        self.container = MockedContainer()

        # Créer l'application avec le container de test
        self.app = create_app(self.container)

        # Créer le client de test
        self.client = TestClient(self.app)
        self.headers = {"X-API-Key": "your-api-key-here"}

        # Garder une référence aux mocks
        self.mock_file_repository = self.container.file_repository()
        self.mock_data_file_repository = self.container.data_file_repository()

    def test_upload_file(self):
        # Préparer un fichier de test
        test_content = b"test file content"
        test_filename = "test_file.nc"

        # Créer un DataFile de test pour le retour du service
        test_data_file = DataFile(
            uid=test_filename,
            source_hash="abc123",
            status=DataFileLifecycle.upload_completed,
        )

        # Simuler l'upload de fichier
        response = self.client.post(
            "/api/v1/files/upload",
            files={"file": (test_filename, test_content)},
            headers=self.headers,
        )

        # Vérifier la réponse
        print(response.json())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["uid"], test_filename)
        self.assertEqual(DataFileLifecycle(data["status"]), test_data_file.status)

        # Vérifier les appels aux repositories
        # self.mock_data_file_repository.find_by_id.assert_called_once()
        # self.mock_data_file_repository.find_by_hash.assert_called_once()
        self.mock_file_repository.upload_file.assert_called_once()

    def tearDown(self):
        # Nettoyer les fichiers temporaires si nécessaire
        if meteo_domain.config.LOCAL_STORAGE_PATH.exists():
            import shutil

            shutil.rmtree(meteo_domain.config.LOCAL_STORAGE_PATH)
