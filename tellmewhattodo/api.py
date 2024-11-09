from collections.abc import Generator
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from tellmewhattodo.models import Alert
from tellmewhattodo.schemas import AlertTable, Base

app = FastAPI(title="Tell Me What To Do API")

engine = create_engine("sqlite:///database.db")
Base.metadata.create_all(engine)


def get_db_session() -> Generator[Session]:
    with Session(engine) as session:
        yield session
        session.commit()


DbDep = Annotated[Session, Depends(get_db_session)]


@app.get("/")
def get_alerts(db: DbDep) -> list[Alert]:
    alerts = db.scalars(
        select(AlertTable).order_by(
            AlertTable.acked,
            AlertTable.created_at.desc(),
            AlertTable.name,
        ),
    )
    return [Alert.model_validate(alert) for alert in alerts]


@app.patch("/{alert_id}")
def ack_alert(db: DbDep, alert_id: str, acked: bool) -> None:  # noqa: FBT001 allow boolean positional arg in API controller
    alert = db.scalar(select(AlertTable).where(AlertTable.id == alert_id))
    if not alert:
        raise HTTPException(status_code=404)
    alert.acked = acked
