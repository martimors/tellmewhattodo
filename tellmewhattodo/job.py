from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.orm import Session

from tellmewhattodo.api import engine
from tellmewhattodo.extractor import BaseExtractor, get_extractors
from tellmewhattodo.schemas import AlertTable

if TYPE_CHECKING:
    from tellmewhattodo.models import Alert


def extract_data(extractors: list[BaseExtractor]) -> None:
    alerts: list[Alert] = []
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
                )
                for alert in alerts
                if alert.id not in existing_ids
            ],
        )
        session.commit()


if __name__ == "__main__":
    extract_data(get_extractors())
