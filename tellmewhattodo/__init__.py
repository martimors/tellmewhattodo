from logging import INFO, basicConfig
from os import getenv

basicConfig(
    level=getenv("LOGLEVEL") or INFO,
    format="%(asctime)s %(levelname)7s %(name)s %(message)s",
    force=True,
)
