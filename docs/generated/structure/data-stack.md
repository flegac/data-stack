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
│   │           └── s3_file_repository.py
│   ├── measure-repository-datafile
│   │   └── src
│   │       └── measure_repository_datafile
│   │           └── data_file_measure_repository.py
│   ├── measure-repository-influxdb
│   │   └── src
│   │       └── measure_repository_influxdb
│   │           ├── influxdb_measure_repository.py
│   │           └── query_mapping.py
│   ├── measure-repository-openmeteo
│   │   └── src
│   │       └── measure_repository_openmeteo
│   │           ├── config.py
│   │           └── open_meteo_measure_repository.py
│   ├── message-queue-kafka
│   │   └── src
│   │       └── message_queue_kafka
│   │           ├── kafka_consumer.py
│   │           ├── kafka_factory.py
│   │           └── kafka_producer.py
│   └── message-queue-redis
│       └── src
│           └── message_queue_redis
│               ├── redis_config.py
│               ├── redis_connection.py
│               ├── redis_consumer.py
│               ├── redis_factory.py
│               └── redis_producer.py
├── connectors
│   ├── celery-connector
│   │   └── src
│   │       └── celery_connector
│   ├── influxdb-connector
│   │   └── src
│   │       └── influxdb_connector
│   │           ├── influxdb_config.py
│   │           └── influx_db_connection.py
│   ├── kafka-connector
│   │   └── src
│   │       └── kafka_connector
│   │           ├── kafka_config.py
│   │           └── kafka_connection.py
│   ├── pg-connector
│   │   └── src
│   │       └── pg_connector
│   │           └── pg_connection.py
│   ├── redis-connector
│   │   └── src
│   │       └── redis_connector
│   └── s3-connector
│       └── src
│           └── s3_connector
│               ├── s3_config.py
│               └── s3_connection.py
└── projects
    ├── aa-common
    │   └── src
    │       └── aa_common
    │           ├── constants.py
    │           └── logger.py
    ├── message-queue
    │   └── src
    │       └── message_queue
    │           ├── memory_mq_backend.py
    │           ├── mq_backend_checker.py
    │           ├── mq_backend.py
    │           ├── mq_consumer.py
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
    │           ├── wires
    │           │   ├── config.py
    │           │   ├── repositories.py
    │           │   └── services.py
    │           └── workers
    │               ├── data_file_ingestion_listener.py
    │               ├── data_file_upload_worker.py
    │               └── measure_ingestion_listener.py
    ├── meteo-backend
    │   └── src
    │       └── meteo_backend
    │           ├── api
    │           │   ├── routes
    │           │   │   ├── files.py
    │           │   │   └── health.py
    │           │   └── schemas
    │           ├── app_factory.py
    │           ├── core
    │           │   ├── application_context.py
    │           │   ├── config
    │           │   │   ├── container.py
    │           │   │   └── settings.py
    │           │   ├── dependencies.py
    │           │   └── security
    │           └── main.py
    └── meteo-domain
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
