"""Настройки бота."""
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки бота."""

    token: str = None
    chat_id: int = None

    class Config:

        env_file = ".env"


settings = Settings()