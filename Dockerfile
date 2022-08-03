FROM python:3.10-slim-bullseye as base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base as builder
# Builder has the build dependencies such as curl and poetry

RUN apt update && apt install -y curl

ENV PIP_DEFAULT_TIMEOUT=100 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH /root/.local/bin:$PATH

COPY poetry.lock pyproject.toml ./
COPY tellmewhattodo/ tellmewhattodo/
RUN poetry install --no-interaction --no-dev

FROM base as final
# Final container doesn't have poetry, curl, pyproject.toml, poetry.lock etc., only necessary code

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/tellmewhattodo/ /app/tellmewhattodo/
COPY tellme.yml .

RUN . .venv/bin/activate
ENV PATH /app/.venv/bin:$PATH
ENTRYPOINT ["tellmewhattodo"]