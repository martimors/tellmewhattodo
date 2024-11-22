import sys
from abc import ABC, abstractmethod
from logging import getLogger
from os import getenv

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from tellmewhattodo.db import get_db_engine
from tellmewhattodo.models import Alert, AlertType
from tellmewhattodo.schemas import AlertTable
from tellmewhattodo.settings import ExtractorJobConfig, Settings

logger = getLogger()


class BaseExtractor(ABC):
    @abstractmethod
    def check(self) -> list[Alert]:
        pass


class GitHubReleaseExtractor(BaseExtractor):
    def __init__(self, repository: str) -> None:
        self.REPOSITORY = repository

    def check(self) -> list[Alert]:
        auth_token = getenv("GITHUB_PAT_TOKEN")
        auth = ("token", auth_token) if auth_token else None
        r = requests.get(
            f"https://api.github.com/repos/{self.REPOSITORY}/releases",
            auth=auth,
            timeout=10,
        )
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logger.exception("Extraction failed for %s", self.REPOSITORY)
            return []

        body = r.json()

        alerts = []
        for release in body:
            if release["prerelease"] or release["draft"]:
                continue
            alerts.append(
                Alert(
                    id=str(release["id"]),
                    name=release.get("name")
                    or f"{self.REPOSITORY}-{release['tag_name']}",
                    description=f"{self.REPOSITORY} released {release['name']}",
                    created_at=release["created_at"],
                    acked=False,
                    url=release["html_url"],
                    alert_type=AlertType.GITHUB,
                ),
            )

        return alerts


def get_extractors(config: ExtractorJobConfig) -> list[BaseExtractor]:
    extractors = []
    for extractor in config.extractors:
        if extractor.type_ == AlertType.GITHUB:
            instance = GitHubReleaseExtractor(extractor.config["repository"])
        else:
            msg = f"Unknown extractor type {extractor.type_}"
            raise ValueError(msg)
        extractors.append(instance)

    return extractors


def extract_data(extractors: list[BaseExtractor]) -> None:
    alerts: list[Alert] = []
    engine = get_db_engine()
    with Session(engine) as session:
        existing_ids = [alert.id for alert in session.scalars(select(AlertTable))]
        for extractor in extractors:
            alerts.extend(extractor.check())
        session.add_all(
            [
                AlertTable(
                    id=alert.id,
                    name=alert.name,
                    created_at=alert.created_at,
                    acked=alert.acked,
                    description=alert.description,
                    url=str(alert.url),
                    alert_type=alert.alert_type,
                )
                for alert in alerts
                if alert.id not in existing_ids
            ],
        )
        session.commit()


if __name__ == "__main__":
    settings = Settings()  # type: ignore[reportCallIssue]
    config = ExtractorJobConfig.from_yaml_file(settings.extractor_job_config_path)
    extract_data(get_extractors(config))
