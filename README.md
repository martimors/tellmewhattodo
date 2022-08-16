```
cat .env.example > .env
poetry install
poetry run tellmewhattodo --help
```

Configuration in [tellme.yml](./tellme.yml) takes presedence, but configuration can also be done with environmental variables prefixed with `TELLME_`. For example, for the storage class, the environment variable `TELLME_STORAGE=S3Storage` could be set.

You can run the app in docker with the production-ready public docker image,

```
docker run -it dingobar/tellmewhattodo:2.1.0-3.10-slim-bullseye check
docker run -it dingobar/tellmewhattodo:2.1.0-3.10-slim-bullseye server
```

Be sure to use [the latest version](https://hub.docker.com/r/dingobar/tellmewhattodo/tags).

## Improvement ideas

- Error handling (currently a village in siberia)
- Backend API
- Helm chart
