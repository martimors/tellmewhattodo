from logging import getLogger
from pathlib import Path

import yaml
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

logger = getLogger(__name__)


class ExtractorJob(BaseModel):
    type: str
    config: dict[str, int | str | float]


class TellMe(BaseSettings):
    extractors: list[ExtractorJob] = []

    model_config = SettingsConfigDict(env_prefix="TELLME_")


def get_config() -> TellMe:
    extractor_config_path = Path.cwd() / "tellme.yml"
    if extractor_config_path.exists() and extractor_config_path.is_file():
        logger.info("Found %s, parsing as config", extractor_config_path)
        with extractor_config_path.open("r") as config:
            extractor_config = TellMe.model_validate(yaml.safe_load(config))
    else:
        logger.warning("Did not find %s, proceeding without", extractor_config_path)
        extractor_config = TellMe()

    logger.debug("Parsed config as %s", str(extractor_config.model_dump()))
    return extractor_config


config = get_config()
