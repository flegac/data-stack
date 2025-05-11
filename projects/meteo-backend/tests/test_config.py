import os
from unittest import TestCase

from meteo_backend.core.config.settings import Settings


class TestSettings(TestCase):
    def setUp(self):
        # Sauvegarder les variables d'environnement originales
        self.original_env = dict(os.environ)

        # Configurer les variables d'environnement pour les tests
        os.environ.update(
            {
                "API_KEY": "your-api-key-here",
                "HOST": "0.0.0.0",
                "PORT": "8000",
                "DEBUG": "true",
                "VERSION": "1.0.0",
                "CORS_ORIGINS": '["http://localhost:3000", "http://localhost:8080"]',
            }
        )

    def tearDown(self):
        # Restaurer les variables d'environnement originales
        os.environ.clear()
        os.environ.update(self.original_env)

    def test_settings_from_env(self):
        settings = Settings()
        self.assertEqual(settings.API_KEY, "your-api-key-here")
        self.assertEqual(settings.APP_HOST, "0.0.0.0")
        self.assertEqual(settings.APP_PORT, 8000)
        self.assertTrue(settings.DEBUG)
        self.assertEqual(settings.APP_VERSION, "1.0.0")
        self.assertEqual(
            settings.CORS_ORIGINS, ["http://localhost:3000", "http://localhost:8080"]
        )

    def test_default_values(self):
        # Supprimer toutes les variables d'environnement de test
        for key in ["API_KEY", "HOST", "PORT", "DEBUG", "VERSION", "CORS_ORIGINS"]:
            os.environ.pop(key, None)

        settings = Settings()
        # Vérifier les valeurs par défaut
        self.assertEqual(settings.APP_HOST, "0.0.0.0")
        self.assertEqual(settings.APP_PORT, 8000)
        self.assertFalse(settings.DEBUG)
        self.assertEqual(settings.APP_VERSION, "1.0.0")
        self.assertEqual(settings.CORS_ORIGINS, ["*"])
