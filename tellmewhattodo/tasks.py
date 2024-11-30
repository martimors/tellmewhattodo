from functools import cache

from celery import Celery
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from tellmewhattodo.extractor import extract_data, get_extractors
from tellmewhattodo.settings import ExtractorJobConfig, Settings


@cache
def get_settings() -> Settings:
    return Settings()


@cache
def get_db_engine() -> Engine:
    settings = get_settings()
    return create_engine(f"sqlite:///{settings.database_location}")


settings = get_settings()
celery = Celery(
    "tasks",
    broker=settings.rabbitmq_dsn,
    broker_connection_retry_on_startup=True,
)


@celery.task(name="extract_alerts")
def extractor_task() -> None:
    extractor_jobs = ExtractorJobConfig.from_yaml_file(
        settings.extractor_job_config_path,
    )
    with Session(get_db_engine()) as db:
        extract_data(get_extractors(extractor_jobs), db)


def run_celery_worker() -> None:
    celery.start(["worker", "-l", "INFO"])


if __name__ == "__main__":
    run_celery_worker()
