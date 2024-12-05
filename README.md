# TMWTD

Simple app with a UI that keeps track of github releases automatically.

Simple ack feature that lets me tick off releases I've already either installed or
want to skip.

For home use.

## Quickstart locally

```sh
poetry install
npm install

# Start in docker
docker compose up --build
```

## Install with helm

```sh
helm upgrade --install tmwtd oci://registry-1.docker.io/dingobar/tmwtd
```

## UI Compile and Hot-Reload for Development

```sh
npm run dev
```

## TODO

- Scheduler (k8s cron using curl)
