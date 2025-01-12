import http
from datetime import UTC, datetime
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
    # Subquery to get the latest event per extractor_id
    sub = select(
        AlertTable,
        func.row_number()
        .over(
            partition_by=AlertTable.extractor_id, order_by=desc(AlertTable.created_at)
        )
        .label("rn"),
    ).subquery()

    # Subquery to find the last acked event name per extractor_id
    last_acked_sub = (
        select(
            AlertTable.extractor_id,
            func.first_value(AlertTable.name)
            .over(
                partition_by=AlertTable.extractor_id,
                order_by=desc(AlertTable.acked_at),
            )
            .label("last_acked_name"),
        )
        .where(AlertTable.acked_at.isnot(None))
        .distinct(AlertTable.extractor_id)
    ).subquery()

    # Main query to fetch the latest alerts with the last_acked_name
    query = (
        select(AlertTable, last_acked_sub.c.last_acked_name)
        .join(sub, AlertTable.id == sub.c.id)
        .outerjoin(
            last_acked_sub,
            AlertTable.extractor_id == last_acked_sub.c.extractor_id,
        )
        .order_by(
            AlertTable.acked_at,
            sub.c.created_at.desc(),
            AlertTable.name,
        )
    )

    if latest_only:
        query = query.where(sub.c.rn == 1)

    results = db.execute(query).all()
    # Add the computed last_acked_name to the Alert model (if required)
    alerts = []
    for alert, last_acked_name in results:
        al = Alert.model_validate(alert)
        al.last_acked_name = last_acked_name
        alerts.append(al)
    return alerts


@app.patch("/{alert_id}")
def ack_alert(db: DbDep, *, alert_id: str, acked: bool) -> None:
    alert = db.scalar(select(AlertTable).where(AlertTable.id == alert_id))
    if not alert:
        raise HTTPException(status_code=404)
    if acked:
        alert.acked_at = datetime.now(UTC)
    else:
        alert.acked_at = None


@app.post("/", status_code=http.HTTPStatus.ACCEPTED)
def start_alerts_check_job() -> None:
    extractor_task.delay()  # type: ignore[reportFunctionMemberAccess]
