"""
Config module for the application.

This module provides the configuration for the application.
"""
import os
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent


class Auth(BaseModel):
    private_key_path: Path = BASE_DIR / "cearts" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR / "cearts" / "jwt-public.pem"
    algorithm: str = "RS256"


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    db_url: str = os.getenv("URL")

    auth_jwt: Auth = Auth()


settings = Settings()
