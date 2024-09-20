from multiprocessing import cpu_count

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
    box: str | None = None
    town: str | None = None
    url: str | None = None
    url_test: str | None = None
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

    # @field_validator("is_debug", mode="before")
    # def build_is_debug(
    #     cls,
    #     value: bool | None,
    #     info: ValidationInfo,
    # ) -> bool:
    #     if value is not None:
    #         return value

    #     return bool(info.data["environment"] == "development")

    # @field_validator("log_level", mode="before")
    # def build_log_level(
    #     cls,
    #     value: str | None,
    #     info: ValidationInfo,
    # ) -> str:
    #     if value is not None:
    #         return value

    #     return "DEBUG" if info.data["is_debug"] else "INFO"
    model_config = ConfigDict(env_prefix="APP_")


class Settings(BaseSettings):
    app_settings: AppSettings = AppSettings()


settings: Settings = Settings()
WEBHOOK_PATH = settings.app_settings.webhook_path.format(settings.app_settings.telegram_token)
WEBHOOK_URL = settings.app_settings.webhook_url.format(WEBHOOK_PATH)
