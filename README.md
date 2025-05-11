# Data-stack

Attempt to create a complete architecture to handle meteorological data.

**short-term (WIP):**

- [X] upload grib/hdf5 `DataFile` (FastAPI)
- [X] archive `DataFile` (S3 / MinIO / Posix)
- [X] manage `DataFile` lifecycle (PostgreSQL, Kafka)
- [X] ingest `DataFile` as a set of `Measurements`
- [X] Efficient temporal access to `Measurements` (InfluxDB)
- [X] Efficient spatial query (PostGIS)

**middle-term (TODO):**

- [ ] Generate graphics, data visualisation, frontend (?)
- [ ] Prediction, machine learning, experiments on data
- [ ] DevOps: packaging, monitoring, scalability (Prometheus, Grafana, Kubernetes)

**personal goals:**

- benchmark different Techs (message queues, databases)
- experiments with code structure / technics

## Documentation

- [Features](./docs/features.md)
- [Glossary](./docs/glossary.md)
- [Technologies](./docs/technologies.md)

## Setup

```bash
# create virtual env
uv venv
```

```bash
# synchronize environment
uv sync --all-packages
```

```bash
# lint, format (pre-commit)
uv run pre-commit run --all-files
```

```bash
# generate docs
uv run scripts/analyze.py
```

```bash
# run server
cd projects/meteo-backend
```

```bash
# test project
uv run coverage run -m pytest
```

```bash
# generate coverage
uv run coverage html -d docs/coverage
```

