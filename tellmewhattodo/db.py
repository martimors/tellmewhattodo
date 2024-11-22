from collections.abc import Generator
from functools import cache

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from tellmewhattodo.schemas import Base


@cache
def get_db_engine() -> Engine:
    engine = create_engine("sqlite:///database.db")
    Base.metadata.create_all(engine)
    return engine


def get_db_session() -> Generator[Session]:
    engine = get_db_engine()
    with Session(engine) as session:
        yield session
        session.commit()
