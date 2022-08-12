```
cat .env.example > .env
poetry install
poetry run tellmewhattodo --help
```

Configuration in [tellme.yml](./tellme.yml) takes presedence, but configuration can also be done with environmental variables prefixed with `TELLME_`. For example, for the storage class, the environment variable `TELLME_STORAGE=S3Storage` could be set.

## Improvement ideas

- Error handling (currently a village in siberia)
- Backend API
- Helm chart
