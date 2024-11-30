from collections.abc import Generator
from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session

from tellmewhattodo.schemas import Base
from tellmewhattodo.settings import Settings


@cache
def get_settings() -> Settings:
    return Settings()


SettingsDep = Annotated[Settings, Depends(get_settings)]


def get_db_engine(settings: SettingsDep) -> Engine:
    engine = create_engine(f"sqlite:///{settings.database_location}")
    Base.metadata.create_all(engine)
    return engine


DbEngineDep = Annotated[Engine, Depends(get_db_engine)]


def get_db_session(engine: DbEngineDep) -> Generator[Session]:
    with Session(engine) as session:
        yield session
        session.commit()


DbDep = Annotated[Session, Depends(get_db_session)]
