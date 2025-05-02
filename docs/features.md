# Features

## Datafile uploader

Given a grib/hdf5 file

- archive it (upload to S3/minio)
- write a DataFile message on `DataFile.ingestion.topic`

```bash
uv run ../src/datafile_uploader.py
```

## Datafile ingestion handler

- Listen for files on `Datafile.ingestion.topic`
- For each variable in the GRIB/HDF5 file, writes all measures on `measure.topic`

```bash
uv run ../src/datafile_ingestion_listener.py
```

## Measure Dispatcher (TODO)

- Listen for measures on `measure.topic`
- dispatch measures by `variable_name` to `{variable_name}.topic`

## Measure Ingester (TODO)

- Listen for measures on `{variable_name}.topic`
- Save it to the `{variable_name}` Measurement (=table) in InfluxDB

## Some application out of measurements ... (TODO)

- graph drawing
- train a predictive model on time series
- ...
