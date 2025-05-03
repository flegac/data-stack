```
data-stack
├── adapters
│   ├── data-file-repository-pg
│   │   └── src
│   │       └── data_file_repository_pg
│   │           ├── data_file_model.py
│   │           └── pg_data_file_repository.py
│   ├── file-repository-posix
│   │   └── src
│   │       └── file_repository_posix
│   │           └── posix_file_repository.py
│   ├── file-repository-s3
│   │   └── src
│   │       └── file_repository_s3
│   │           ├── s3_config.py
│   │           └── s3_file_repository.py
│   ├── measure-repository-datafile
│   │   └── src
│   │       └── measure_repository_datafile
│   │           ├── data_file_measure_reader.py
│   │           ├── data_file_measure_repository.py
│   │           └── data_file_measure_writer.py
│   ├── measure-repository-influxdb
│   │   └── src
│   │       └── measure_repository_influxdb
│   │           ├── influxdb_config.py
│   │           └── influxdb_measure_repository.py
│   ├── measure-repository-openmeteo
│   │   └── src
│   │       └── measure_repository_openmeteo
│   │           ├── config.py
│   │           ├── open_meteo_measure_reader.py
│   │           └── open_meteo_measure_repository.py
│   └── message-queue-kafka
│       └── src
│           └── message_queue_kafka
│               ├── kafka_config.py
│               ├── kafka_consumer.py
│               ├── kafka_factory.py
│               └── kafka_producer.py
└── projects
    ├── aa-common
    │   └── src
    │       └── aa_common
    │           └── constants.py
    ├── message-queue
    │   └── src
    │       └── message_queue
    │           ├── memory_mq_factory.py
    │           ├── mq_consumer.py
    │           ├── mq_factory.py
    │           ├── mq_producer.py
    │           ├── mq_topic.py
    │           └── serializer.py
    ├── meteo-app
    │   └── src
    │       └── meteo_app
    │           ├── config.py
    │           ├── datafile_ingestion_listener.py
    │           ├── datafile_uploader.py
    │           ├── exports
    │           ├── measure_ingestion_listener.py
    │           ├── open_meteo_producer_app.py
    │           ├── server_app.py
    │           ├── wires
    │           │   ├── config.py
    │           │   ├── repositories.py
    │           │   └── services.py
    │           └── workers
    │               ├── data_file_ingestion_listener.py
    │               ├── data_file_upload_worker.py
    │               └── measure_ingestion_listener.py
    └── meteo-measures
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
