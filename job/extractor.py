from abc import ABC, abstractmethod
import datetime
from os import getenv
from typing import Any
import requests
from models.alert import Alert


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
        )
        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            print(e)
            return []

        body: list[dict[str, Any]] = r.json()

        alerts = []
        for release in body:
            if release["prerelease"] or release["draft"]:
                continue
            alerts.append(
                Alert(
                    id=str(release["id"]),
                    name=release["name"],
                    description=f"{self.REPOSITORY} released {release['name']}",
                    datetime=release["created_at"],
                    active=True,
                    url=release["html_url"],
                )
            )

        return alerts
