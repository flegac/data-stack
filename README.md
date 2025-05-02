# Data-stack

Attempt to create a complete architecture to handle meteorological data.

**short-term (WIP):**

- [ ] upload grib/hdf5 `DataFile` (FastAPI)
- [X] archive `DataFile` (S3 / MinIO / Posix)
- [X] manage `DataFile` lifecycle (PostgreSQL, Kafka)
- [X] ingest `DataFile` as a set of `Measurements`
- [ ] Efficient temporal access to `Measurements` (InfluxDB)
- [ ] Efficient spatial query (PostGIS?)

**middle-term (TODO):**

- [ ] Generate graphics, data visualisation, frontend (?)
- [ ] Prediction, machine learning, experiments on data
- [ ] DevOps: packaging, monitoring, scalability (Prometheus, Grafana, Kubernetes) 

**personal goals:**

- benchmark different Techs (message queues, databases)
- experiments with code organisation / technics

## Documentation

- [Features](./docs/features.md)
- [Glossary](./docs/glossary.md)
- [Technologies](./docs/technologies.md)

## Setup

```bash
# create/update virtual env
uv venv
```

```bash
# synchronize environment
uv sync --all-packages
```

```bash
# lint, format, analyze (pre-commit)
uv run pre-commit run --all-files
```

```bash
# generate docs
uv run scripts/analyze.py
```
