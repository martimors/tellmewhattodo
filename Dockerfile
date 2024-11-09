FROM python:3.11-alpine AS base

WORKDIR /var/app
COPY requirements.txt requirements.txt
COPY tellmewhattodo tellmewhattodo
RUN pip install -r requirements.txt

ENTRYPOINT [ "fastapi", "run", "tellmewhattodo/api.py", "--workers", "4" ]