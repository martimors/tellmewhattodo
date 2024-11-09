from datetime import datetime

from pydantic import AnyHttpUrl, BaseModel, ConfigDict


class Alert(BaseModel):
    id: str
    name: str
    created_at: datetime
    acked: bool = False
    description: str | None = None
    url: AnyHttpUrl | None = None

    model_config = ConfigDict(from_attributes=True)
