from pydantic import BaseModel, AnyHttpUrl
from datetime import datetime


class Alert(BaseModel):
    id: str
    name: str
    description: str
    datetime: datetime
    active: bool = True
    url: AnyHttpUrl = None
