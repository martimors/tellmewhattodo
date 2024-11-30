FROM python:3.13-slim

WORKDIR /var/app
COPY requirements.txt requirements.txt
COPY tellmewhattodo tellmewhattodo
RUN pip install -r requirements.txt && rm requirements.txt
ENV API_ROOT_PATH=/api

COPY entrypoint.sh .

ENTRYPOINT [ "./entrypoint.sh" ]
EXPOSE 8000