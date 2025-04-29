# Data-stack

Putting together a data stack with Python to handle meteorological data.

## Setup

```bash
rm .venv
uv venv
uv sync --all-packages 
```

## Technologies

Long term storage / archiving:

- S3 (minio)
- NetCDF / HDF5


Short term storage / querying:

- InfluxDB

Metadata DB:

- PostgreSQL

Message brokers:

- Kafka

Data processing:

- xarray : data structures
- dask : distributed computing
- xarray-simlab : simulations

Data sources:

- OpenMeteo API

Hexagonal architecture:

- https://injector.readthedocs.io/en/latest/

Tools:

- uv: package manager
- unittest: unit testing
