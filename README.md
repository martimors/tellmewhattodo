# TMWTD

Simple app with a UI that keeps track of github releases automatically.

Simple ack feature that lets me tick off releases I've already either installed or
want to skip.

For home use.

## Quickstart locally

```sh
cp .env.example .env
poetry install
npm install

# Start in docker
docker compose up --build
```

## Install with helm

```sh
helm upgrade --install tmwtd oci://registry-1.docker.io/dingobar/tellmewhattodo
```

See [here](./charts/tmwtd/values.yaml) for possible values.

## UI Compile and Hot-Reload for Development

```sh
npm run dev
```

If the backend contract changes, the API client must be regenerated,

```sh
# Regenerate API client code for frontend
npx @hey-api/openapi-ts -i http://localhost:8000/openapi.json -o ui/src/client -c @hey-api/client-fetch
```
