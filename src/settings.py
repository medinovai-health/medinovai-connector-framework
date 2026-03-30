"""Application settings from environment (no secrets embedded)."""

from functools import lru_cache
from typing import Optional

from pydantic import AliasChoices, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime configuration for the connector framework service."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    service_name: str = Field(
        default="medinovai-connector-framework",
        validation_alias=AliasChoices("SERVICE_NAME", "service_name"),
    )
    port: int = Field(default=8000, validation_alias=AliasChoices("PORT", "port"))
    registry_url: str = Field(
        default="http://medinovai-registry.medinovai:8000",
        validation_alias=AliasChoices("REGISTRY_URL", "registry_url"),
    )
    integration_gateway_url: str = Field(
        default="http://medinovai-integration-gateway:8000",
        validation_alias=AliasChoices(
            "INTEGRATION_GATEWAY_URL",
            "integration_gateway_url",
        ),
    )
    secrets_prefix: str = Field(
        default="medinovai/connector-framework",
        validation_alias=AliasChoices("MOS_SECRETS_PREFIX", "secrets_prefix"),
    )
    log_level: str = Field(
        default="INFO",
        validation_alias=AliasChoices("MOS_LOG_LEVEL", "log_level"),
    )
    config_path: Optional[str] = Field(
        default=None,
        validation_alias=AliasChoices("MOS_CONFIG_PATH", "config_path"),
    )


@lru_cache
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()

