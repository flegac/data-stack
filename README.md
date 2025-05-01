# Data-stack

Putting together a data stack with Python to handle meteorological data.

## Setup

```bash
# rm .venv
uv venv
uv sync --all-packages
```

## Running

### Datafile uploader

Given a grib/hdf5 file

- archive it (upload to S3/minio)
- write a DataFile message on `DataFile.ingestion.topic`

```bash
uv run ./src/datafile_uploader.py
```

### Datafile ingestion handler

- Listen for files on `Datafile.ingestion.topic`
- For each variable in the GRIB/HDF5 file, writes all measures on `measure.topic`

```bash
uv run ./src/datafile_ingestion_listener.py
```

### Measure Dispatcher (TODO)

- Listen for measures on `measure.topic`
- dispatch measures by `variable_name` to `{variable_name}.topic`

### Measure Ingester (TODO)

- Listen for measures on `{variable_name}.topic`
- Save it to the `{variable_name}` Measurement (=table) in InfluxDB

### Some application out of measurements ... (TODO)

- graph drawing
- train a predictive model on time series
- ...

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

- https://github.com/ets-labs/python-dependency-injector
- https://injector.readthedocs.io/en/latest/

Tools:

- uv: package manager
- unittest: unit testing
