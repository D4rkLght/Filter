from multiprocessing import cpu_count
from pathlib import Path

from pydantic import ConfigDict, ValidationInfo, field_validator
from pydantic.networks import PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Base(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        env_file_encoding="utf-8"
    )


class AppSettings(Base):
    wsgi_app_path: str = "bot.main:app"
    wsgi_host: str = "0.0.0.0"
    wsgi_port: str = "8000"
    wsgi_workers: int = cpu_count()
    is_debug: bool | None = None
    log_level: str | None = None
    telegram_token: str = "token"
    webhook_mode: bool | None = False
    webhook_url: str | None = None
    webhook_path: str | None = None
    webhook_secret_key: str | None = None
    telegram_user_id: int | None = None

    @property
    def service_name(
        self,
    ) -> str:
        return self.docs_name

    model_config = ConfigDict(env_prefix="APP_")


class Settings(BaseSettings):
    app_settings: AppSettings = AppSettings()


settings: Settings = Settings()
WEBHOOK_PATH = settings.app_settings.webhook_path.format(settings.app_settings.telegram_token)
WEBHOOK_URL = settings.app_settings.webhook_url.format(WEBHOOK_PATH)
TIME_IN_SECONDS = 60
