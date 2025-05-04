from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Server Settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    VERSION: str = "1.0.0"
    CORS_ORIGINS: list[str] = ["*"]
    LOCAL_STORAGE_PATH: Path = Path("/tmp/meteo-files")

    # API Settings
    API_VERSION: str = "v1"
    API_KEY: str = "your-api-key-here"
    DEBUG: bool = False

    # S3 Settings
    S3_REGION: str = "eu-west-1"
    S3_ENDPOINT: str = "http://localhost:9000"
    S3_BUCKET: str = "meteo-files"
    S3_ACCESS_KEY: str = "admin"
    S3_SECRET_KEY: str = "adminpassword"

    # Kafka Settings
    KAFKA_BROKER_URL: str = "localhost:9092"
    KAFKA_GROUP_ID: str = "meteo-group"

    # PostgreSQL settings pour DataFileRepository
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "meteo-db"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "adminpassword"

    # InfluxDB Settings
    INFLUXDB_URL: str = "http://localhost:8086"
    INFLUXDB_TOKEN: str = "server-token"
    INFLUXDB_ORG: str = "your-org"
    INFLUXDB_BUCKET: str = "meteo"
    INFLUXDB_USER: str = "admin"
    INFLUXDB_PASSWORD: str = "adminpassword"

    class Config:
        env_file = ".env"
