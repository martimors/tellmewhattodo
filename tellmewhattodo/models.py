from datetime import datetime
from enum import StrEnum

from pydantic import AnyHttpUrl, BaseModel, ConfigDict, computed_field


class AlertType(StrEnum):
    GITHUB = "github"
    DOCKERHUB = "dockerhub"
    DOCKERHUB_HELM = "docker_helm"


class Alert(BaseModel):
    id: str
    extractor_id: str
    name: str
    created_at: datetime
    alert_type: AlertType
    acked_at: datetime | None = None
    description: str | None = None
    url: AnyHttpUrl | None = None
    last_acked_name: str | None = None

    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def acked(self) -> bool:
        return self.acked_at is not None
