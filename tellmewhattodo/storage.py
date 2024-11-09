from abc import ABC, abstractmethod

from tellmewhattodo.models import Alert


class AbstractStorage(ABC):
    @abstractmethod
    def save(self, alerts: list[Alert]) -> None:
        pass

    @abstractmethod
    def read(self) -> None:
        pass

    @abstractmethod
    def ack(self, alert: Alert) -> None:
        pass


class SqliteStorage(AbstractStorage):
    def save(self, alerts: list[Alert]) -> None:
        return super().save(alerts)

    def read(self) -> None:
        return super().read()

    def ack(self, alert: Alert) -> None:
        return super().ack(alert)
