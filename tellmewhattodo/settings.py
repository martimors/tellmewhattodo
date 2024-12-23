from __future__ import annotations

from abc import abstractmethod
from enum import StrEnum
from logging import getLogger
from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, Field, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


class ArtifactType(StrEnum):
    HELM = "helm"


class AbstractJobConfig(BaseModel):
    @property
    @computed_field
    @abstractmethod
    def extractor_id(self) -> str:
        pass


class DockerHubExtractorJobConfig(AbstractJobConfig):
    type_: Literal["oci"] = Field(alias="type")
    repository: str
    artifact_type: ArtifactType

    @property
    def extractor_id(self) -> str:
        return (
            f"{self.type_}:{self.artifact_type}:{self.repository.replace("/", "-")}"
        ).lower()


class GitHubExtractorJobConfig(AbstractJobConfig):
    type_: Literal["github"] = Field(alias="type")
    repository: str

    @property
    def extractor_id(self) -> str:
        return f"{self.type_}:{self.repository.replace("/", "-")}".lower()


class Settings(BaseSettings):
    extractor_job_config_path: Path = Path.cwd() / "extractors.yml"
    rabbitmq_host: str = "localhost"
    rabbitmq_username: str = "guest"
    rabbitmq_password: SecretStr | None = None
    rabbitmq_port: int = 5672
    database_location: str = "database.db"

    model_config = SettingsConfigDict(env_prefix="TELLME_")


class ExtractorJobConfig(BaseModel):
    extractors: list[GitHubExtractorJobConfig | DockerHubExtractorJobConfig]

    @classmethod
    def from_yaml_file(cls, extractor_job_config_path: Path) -> ExtractorJobConfig:
        logger.info("Parsing extractor config file at %s", extractor_job_config_path)
        with extractor_job_config_path.open("r") as config:
            return ExtractorJobConfig.model_validate(yaml.safe_load(config))
