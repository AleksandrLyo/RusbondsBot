"""Настройки бота."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки бота."""

    token: str = None

    class Config:

        env_file = ".env"


settings = Settings()