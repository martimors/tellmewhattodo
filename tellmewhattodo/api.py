import http
from os import environ

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select

from tellmewhattodo.dependencies import DbDep
from tellmewhattodo.models import Alert
from tellmewhattodo.schemas import AlertTable
from tellmewhattodo.tasks import extractor_task

origins = environ.get("CORS_ORIGIN") or []

app = FastAPI(
    title="Tell Me What To Do API",
    root_path=environ.get("API_ROOT_PATH") or "",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["GET", "PATCH"],
)



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


@app.post("/", status_code=http.HTTPStatus.ACCEPTED)
def start_alerts_check_job() -> None:
    extractor_task.delay()
