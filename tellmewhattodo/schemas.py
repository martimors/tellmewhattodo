from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AlertTable(Base):
    __tablename__ = "alert"
    id: Mapped[str] = mapped_column(primary_key=True)
    extractor_id: Mapped[str]
    name: Mapped[str]
    created_at: Mapped[datetime]
    acked_at: Mapped[datetime | None] = mapped_column(nullable=True)
    description: Mapped[str | None] = mapped_column(nullable=True)
    url: Mapped[str | None] = mapped_column(nullable=True)
    alert_type: Mapped[str]
