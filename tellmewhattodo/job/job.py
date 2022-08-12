from threading import local
import pandas as pd
from tellmewhattodo.job.extractor import get_extractors
from tellmewhattodo.job.storage import client


def main():
    storage_client = client()
    extractors = get_extractors()

    alerts = []
    for extractor in extractors:
        alerts.extend(extractor.check())

    local_alerts = storage_client.read()
    local_alerts["id"] = local_alerts["id"]
    new_alerts = pd.DataFrame([alert.dict() for alert in alerts])
    if not new_alerts.empty:
        # new_alerts = {alert.id for alert in alerts} - set(local_alerts["id"].unique())
        all_alerts = pd.concat(
            [local_alerts, new_alerts.loc[~new_alerts["id"].isin(local_alerts["id"])]]
        )
    else:
        all_alerts = local_alerts

    storage_client.write(all_alerts)
