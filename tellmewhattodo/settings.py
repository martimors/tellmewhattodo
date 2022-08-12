from pathlib import Path
from typing import Union
from pydantic import BaseModel
import yaml


class ExtractorJob(BaseModel):
    type: str
    config: dict[str, Union[int, str, float]]


class TellMe(BaseModel):
    version: int
    storage: str
    extractors: list[ExtractorJob]


def get_config() -> TellMe:
    extractor_config_path = Path.cwd() / "tellme.yml"

    with open(extractor_config_path) as config:
        extractor_config = TellMe.parse_obj(yaml.safe_load(config))

    return extractor_config


config = get_config()
