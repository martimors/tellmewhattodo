import http
from os import environ

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import desc, func, select

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
def get_alerts(db: DbDep, *, latest_only: bool = True) -> list[Alert]:
    sub = select(
        AlertTable,
        func.row_number()
        .over(
            partition_by=AlertTable.extractor_id, order_by=desc(AlertTable.created_at)
        )
        .label("rn"),
    ).subquery()
    query = (
        select(AlertTable)
        .join(sub, AlertTable.id == sub.c.id)
        .where(sub.c.rn == 1)
        .order_by(
            sub.c.acked,
            sub.c.created_at.desc(),
            sub.c.name,
        )
    )
    if latest_only:
        query = query.where(sub.c.rn == 1)
    alerts = db.scalars(query)
    return [Alert.model_validate(alert) for alert in alerts]


@app.patch("/{alert_id}")
def ack_alert(db: DbDep, *, alert_id: str, acked: bool) -> None:
    alert = db.scalar(select(AlertTable).where(AlertTable.id == alert_id))
    if not alert:
        raise HTTPException(status_code=404)
    alert.acked = acked


@app.post("/", status_code=http.HTTPStatus.ACCEPTED)
def start_alerts_check_job() -> None:
    extractor_task.delay()  # type: ignore[reportFunctionMemberAccess]
