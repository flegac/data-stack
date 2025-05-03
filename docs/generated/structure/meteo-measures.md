```
meteo-measures
└── src
    └── meteo_measures
        ├── config.py
        └── domain
            ├── entities
            │   ├── coordinate.py
            │   ├── datafile_lifecycle.py
            │   ├── data_file.py
            │   ├── data_file_serializer.py
            │   ├── measure_query.py
            │   ├── measures
            │   │   ├── location.py
            │   │   ├── measurement.py
            │   │   ├── measure_serializer.py
            │   │   ├── measure_series.py
            │   │   ├── period.py
            │   │   └── sensor.py
            │   ├── meta_data_file.py
            │   └── variable.py
            ├── ports
            │   ├── data_file_repository.py
            │   ├── file_repository.py
            │   ├── measure_reader.py
            │   ├── measure_repository.py
            │   └── measure_writer.py
            └── services
                ├── data_file_creation_service.py
                ├── data_file_ingestion_service.py
                ├── data_file_messaging_service.py
                └── data_file_upload_service.py
```
