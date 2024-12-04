from __future__ import annotations

from logging import getLogger
from pathlib import Path

import yaml
from pydantic import BaseModel, Field, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

from tellmewhattodo.models import AlertType

logger = getLogger(__name__)


class ExtractorJob(BaseModel):
    type_: AlertType = Field(alias="type")
    config: dict[str, str]


class Settings(BaseSettings):
    extractor_job_config_path: Path = Path.cwd() / "extractors.yml"
    rabbitmq_host: str = "localhost"
    rabbitmq_username: str = "guest"
    rabbitmq_password: SecretStr | None = None
    rabbitmq_port: int = 5672
    database_location: str = "database.db"

    model_config = SettingsConfigDict(env_prefix="TELLME_")


class ExtractorJobConfig(BaseModel):
    extractors: list[ExtractorJob]

    @classmethod
    def from_yaml_file(cls, extractor_job_config_path: Path) -> ExtractorJobConfig:
        logger.info("Parsing extractor config file at %s", extractor_job_config_path)
        with extractor_job_config_path.open("r") as config:
            return ExtractorJobConfig.model_validate(yaml.safe_load(config))
