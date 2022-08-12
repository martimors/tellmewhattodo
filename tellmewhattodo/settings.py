from pathlib import Path
from typing import Union
from pydantic import BaseModel, BaseSettings
import yaml
from logging import getLogger

logger = getLogger(__name__)


class ExtractorJob(BaseModel):
    type: str
    config: dict[str, Union[int, str, float]]


class TellMe(BaseSettings):
    version: int = None
    storage: str = None
    extractors: list[ExtractorJob] = []

    class Config:
        env_prefix = "TELLME_"


def get_config() -> TellMe:
    extractor_config_path = Path.cwd() / "tellme.yml"
    if extractor_config_path.exists() and extractor_config_path.is_file():
        logger.info("Found %s, parsing as config", extractor_config_path)
        with open(extractor_config_path) as config:
            extractor_config = TellMe.parse_obj(yaml.safe_load(config))
    else:
        logger.warning("Did not find %s, proceeding without", extractor_config_path)
        extractor_config = TellMe()

    logger.debug("Parsed config as %s", str(extractor_config.dict()))
    return extractor_config


config = get_config()
