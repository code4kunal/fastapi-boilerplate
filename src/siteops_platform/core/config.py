"""12-factor settings via environment (Pydantic Settings v2)."""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = Field(default="local", validation_alias="APP_ENV")
    app_name: str = Field(default="Siteops Platform", validation_alias="APP_NAME")
    log_level: str = Field(default="INFO", validation_alias="LOG_LEVEL")
    api_prefix: str = Field(default="/api/v1", validation_alias="API_PREFIX")
    database_url: str = Field(
        default="postgresql+asyncpg://app:app@localhost:5432/app",
        validation_alias="DATABASE_URL",
    )
    cors_origins: str = Field(default="*", validation_alias="CORS_ORIGINS")
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")
    jwt_secret_key: str = Field(default="change-me", validation_alias="JWT_SECRET_KEY")
    jwt_access_ttl_seconds: int = Field(default=900, validation_alias="JWT_ACCESS_TTL_SECONDS")
    jwt_refresh_ttl_seconds: int = Field(default=604_800, validation_alias="JWT_REFRESH_TTL_SECONDS")
    auth_demo_user: str = Field(default="demo", validation_alias="AUTH_DEMO_USER")
    auth_demo_pass: str = Field(default="demo", validation_alias="AUTH_DEMO_PASS")
    otel_exporter_otlp_endpoint: Optional[str] = Field(default=None, validation_alias="OTEL_EXPORTER_OTLP_ENDPOINT")
    otel_service_name: str = Field(default="siteops_platform", validation_alias="OTEL_SERVICE_NAME")

    @computed_field  # type: ignore[prop-decorator]
    @property
    def database_url_sync(self) -> str:
        u = self.database_url
        if u.startswith("postgresql+asyncpg"):
            return u.replace("postgresql+asyncpg://", "postgresql+psycopg://", 1)
        if u.startswith("sqlite+aiosqlite"):
            return u.replace("sqlite+aiosqlite://", "sqlite://", 1)
        return u


@lru_cache
def get_settings() -> Settings:
    return Settings()