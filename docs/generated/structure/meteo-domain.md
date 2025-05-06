```
meteo-domain
└── src
    └── meteo_domain
        ├── config.py
        ├── entities
        │   ├── datafile_lifecycle.py
        │   ├── data_file.py
        │   ├── data_file_serializer.py
        │   ├── measures
        │   │   ├── location.py
        │   │   ├── measurement.py
        │   │   ├── measure_query.py
        │   │   ├── measure_serializer.py
        │   │   ├── measure_series.py
        │   │   ├── period.py
        │   │   └── sensor.py
        │   ├── meta_data_file
        │   │   ├── coordinate.py
        │   │   ├── meta_data_file.py
        │   │   └── variable.py
        │   └── workspace
        │       └── workspace.py
        ├── ports
        │   ├── data_file_repository.py
        │   ├── file_repository.py
        │   ├── measure_repository.py
        │   └── workspace_repository.py
        └── services
            ├── data_file_creation_service.py
            ├── data_file_ingestion_service.py
            ├── data_file_messaging_service.py
            ├── data_file_upload_service.py
            └── workspace_service.py
```
