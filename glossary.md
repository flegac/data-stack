# Glossary (wip)

## File

- RawFile: binary (or text) file identified by a "key" and a "bucket" (S3 terminology) 
- FileRepository: abstract class to synchronize local/remote files

## Measurement

### Ingestion

- DataFile: track the state of a GRIB/HDF5 file, containing measurements
- TaskStatus: list of possible status for a DataFile
- DataFileRepository: abstract class to manage DataFile (create, search, update status)

### Exploitation

- MeasureType: list of supported measure types (temperature, atm. pressure, pluviometry etc.)
- Sensor: source of a measure
- Measure: a value and a MeasureType
- MeasureSeries: a batch of measures (in memory equivalent to a GRIB/HDF5 file)
- MeasureReader: abstract class that provides a sequence of MeasureSeries
- MeasureWriter: abstract class to write MeasureSeries into a repository
