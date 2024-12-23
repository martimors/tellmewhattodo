import re
from abc import ABC, abstractmethod
from collections.abc import Generator
from logging import getLogger
from os import getenv
from typing import Any

import requests
from sqlalchemy import select
from sqlalchemy.orm import Session

from tellmewhattodo.models import Alert, AlertType
from tellmewhattodo.schemas import AlertTable
from tellmewhattodo.settings import (
    DockerHubExtractorJobConfig,
    ExtractorJobConfig,
    GitHubExtractorJobConfig,
)

logger = getLogger()


class BaseExtractor(ABC):
    @abstractmethod
    def check(self) -> list[Alert]:
        pass


class GitHubReleaseExtractor(BaseExtractor):
    def __init__(self, config: GitHubExtractorJobConfig) -> None:
        self.config = config

    def check(self) -> list[Alert]:
        auth_token = getenv("GITHUB_PAT_TOKEN")
        auth = ("token", auth_token) if auth_token else None
        r = requests.get(
            f"https://api.github.com/repos/{self.config.repository}/releases/latest",
            auth=auth,
            timeout=10,
        )
        try:
            r.raise_for_status()
        except requests.HTTPError:
            logger.exception("Extraction failed for %s", self.config.repository)
            return []

        release = r.json()

        if release["prerelease"] or release["draft"]:
            return []
        alert = Alert(
            id=str(release["id"]),
            extractor_id=self.config.extractor_id,
            name=release.get("name")
            or f"{self.config.repository}-{release['tag_name']}",
            description=f"{self.config.repository} released "
            f"{release['name']} on GitHub",
            created_at=release["created_at"],
            acked=False,
            url=release["html_url"],
            alert_type=AlertType.GITHUB,
        )

        return [alert]


class DockerHubExtractor(BaseExtractor):
    def __init__(self, config: DockerHubExtractorJobConfig) -> None:
        self.config = config

    def _get_paginated_tags(self) -> Generator[list[dict[Any, Any]], None]:
        next_page = f"https://hub.docker.com/v2/repositories/{self.config.repository}/tags?page_size=100"
        while next_page is not None:
            r = requests.get(
                next_page,
                timeout=10,
            )
            try:
                r.raise_for_status()
            except requests.HTTPError:
                logger.exception("Extraction failed for %s", self.config.repository)

            t = r.json()

            next_page = t.get("next")
            yield t["results"]

    @staticmethod
    def _is_extended_plain_semver(version: str) -> bool:
        extended_semver_pattern = r"^(0|[1-9]\d*)(\.(0|[1-9]\d*))*$"
        return bool(re.match(extended_semver_pattern, version))

    @staticmethod
    def _semver_sort_key(tag: dict[Any, Any]) -> tuple[int, ...]:
        parts = tag["name"].split(".")
        return tuple(int(part) for part in parts)

    def check(self) -> list[Alert]:
        tags = []
        for tag in self._get_paginated_tags():
            tags.extend(tag)
        chart_tags = [t for t in tags if t["content_type"] == self.config.artifact_type]
        semver_tags = [
            t for t in chart_tags if self._is_extended_plain_semver(t["name"])
        ]
        sorted_tags = sorted(semver_tags, key=self._semver_sort_key)
        latest_tag = sorted_tags[-1]
        alert = Alert(
            id=str(latest_tag["id"]),
            name=f"{latest_tag['name']}",
            extractor_id=self.config.extractor_id,
            created_at=latest_tag["last_updated"],
            alert_type=AlertType.DOCKERHUB_HELM,
            acked=False,
            description=(
                f"{self.config.artifact_type} {self.config.repository} released "
                f"{latest_tag['name']} on Docker Hub"
            ),
            url=f"https://hub.docker.com/r/{self.config.repository}/tags",  # type: ignore[reportArgumentType]
        )

        return [alert]


def get_extractors(config: ExtractorJobConfig) -> list[BaseExtractor]:
    extractors = []
    for extractor in config.extractors:
        if isinstance(extractor, GitHubExtractorJobConfig):
            instance = GitHubReleaseExtractor(extractor)
        elif isinstance(extractor, DockerHubExtractorJobConfig):
            instance = DockerHubExtractor(extractor)
        else:
            msg = f"Unknown extractor type {extractor.type_}"
            raise TypeError(msg)
        extractors.append(instance)

    return extractors


def extract_data(extractors: list[BaseExtractor], db: Session) -> None:
    alerts: list[Alert] = []
    existing_ids = [alert.id for alert in db.scalars(select(AlertTable))]
    for extractor in extractors:
        alerts.extend(extractor.check())
    db.add_all(
        [
            AlertTable(
                id=alert.id,
                extractor_id=alert.extractor_id,
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
    db.commit()
