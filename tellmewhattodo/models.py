from datetime import datetime
from enum import StrEnum

from pydantic import AnyHttpUrl, BaseModel, ConfigDict


class AlertType(StrEnum):
    GITHUB = "github"


class Alert(BaseModel):
    id: str
    name: str
    created_at: datetime
    alert_type: AlertType
    acked: bool = False
    description: str | None = None
    url: AnyHttpUrl | None = None

    model_config = ConfigDict(from_attributes=True)
