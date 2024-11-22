from logging import getLogger

from celery import Celery
from celery.utils.log import get_task_logger

from tellmewhattodo.extractor import extract_data, get_extractors
from tellmewhattodo.settings import ExtractorJobConfig, Settings

logger = get_task_logger(__name__)
settings = Settings()
celery = Celery(
    "tasks",
    broker=settings.rabbitmq_dsn,
    broker_connection_retry_on_startup=False,
)


@celery.task(name="extract_alerts")
def extractor_task() -> None:
    logger.info("Starting extractor task")
    extractor_jobs = ExtractorJobConfig.from_yaml_file(
        settings.extractor_job_config_path,
    )
    extract_data(get_extractors(extractor_jobs))


def run_celery_worker() -> None:
    celery.start(["worker"])


if __name__ == "__main__":
    run_celery_worker()
