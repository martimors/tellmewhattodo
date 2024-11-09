import sys
from abc import ABC, abstractmethod
from logging import getLogger
from os import getenv

import requests

from tellmewhattodo.models import Alert
from tellmewhattodo.settings import config

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
                ),
            )

        return alerts


def get_extractors() -> list[BaseExtractor]:
    extractors = []
    for extractor in config.extractors:
        instance = getattr(sys.modules[__name__], extractor.type)(**extractor.config)
        extractors.append(instance)

    return extractors
