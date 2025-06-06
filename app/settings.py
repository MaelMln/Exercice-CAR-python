from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    """Paramètres globaux chargés depuis l’environnement (.env)."""

    host: str = "0.0.0.0"
    port: int = 8000
    data_path: str = "data/cars.json"
    finish_distance: int = 100
    allowed_origins: List[str] = ["*"]

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()