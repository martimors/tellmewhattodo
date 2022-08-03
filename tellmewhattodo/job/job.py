from os import getenv
import pandas as pd
from tellmewhattodo.job.extractor import BaseExtractor, GitHubReleaseExtractor
from tellmewhattodo.job.storage import LocalStorage, S3Storage

STORAGE_CLASS_NAME = getenv("STORAGE_CLASS")
if STORAGE_CLASS_NAME == "S3Storage":
    STORAGE_CLASS = S3Storage("mmo-test")
elif STORAGE_CLASS_NAME == "LocalStorage":
    STORAGE_CLASS = LocalStorage()
elif STORAGE_CLASS_NAME is None:
    print("STORAGE_CLASS env variable not given, defaulting to LocalStorage")
    STORAGE_CLASS = LocalStorage()
else:
    raise ValueError(f"Storage class {STORAGE_CLASS_NAME} not found")


def main():
    extractors: list[BaseExtractor] = []
    extractors.append(GitHubReleaseExtractor("dingobar/charts"))
    extractors.append(GitHubReleaseExtractor("apache/airflow"))
    extractors.append(GitHubReleaseExtractor("jupyterhub/zero-to-jupyterhub-k8s"))
    extractors.append(GitHubReleaseExtractor("mlflow/mlflow"))
    extractors.append(GitHubReleaseExtractor("meltano/meltano"))

    alerts = []
    for extractor in extractors:
        alerts.extend(extractor.check())

    local_alerts = STORAGE_CLASS.read()
    new_alerts = pd.DataFrame([alert.dict() for alert in alerts])
    # new_alerts = {alert.id for alert in alerts} - set(local_alerts["id"].unique())
    all_alerts = pd.concat(
        [local_alerts, new_alerts.loc[~new_alerts["id"].isin(local_alerts["id"])]]
    )

    STORAGE_CLASS.write(all_alerts)


if __name__ == "__main__":
    main()
