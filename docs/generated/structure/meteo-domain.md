```
Structure du dossier
Le num�ro de s�rie du volume est C4D9-4B96
C:\USERS\FLO\DOCUMENTS\WORKSPACE\DATA-STACK\PROJECTS\METEO-DOMAIN
|   .python-version
|   pyproject.toml
|   README.md
|   
+---src
|   \---meteo_domain
|       |   config.py
|       |   utils.py
|       |   __init__.py
|       |   
|       +---entities
|       |   |   datafile.py
|       |   |   datafile_lifecycle.py
|       |   |   datafile_serializer.py
|       |   |   measure_query.py
|       |   |   sensor.py
|       |   |   workspace.py
|       |   |   __init__.py
|       |   |   
|       |   +---geo_spatial
|       |   |   |   location.py
|       |   |   |   location_area.py
|       |   |   |   with_location.py
|       |   |   |   __init__.py
|       |   |   |   
|       |   |   \---__pycache__
|       |   |           location.cpython-313.pyc
|       |   |           location_area.cpython-313.pyc
|       |   |           with_location.cpython-313.pyc
|       |   |           __init__.cpython-313.pyc
|       |   |           
|       |   +---measurement
|       |   |   |   measurement.py
|       |   |   |   measure_serializer.py
|       |   |   |   measure_series.py
|       |   |   |   sensor_serializer.py
|       |   |   |   __init__.py
|       |   |   |   
|       |   |   \---__pycache__
|       |   |           measurement.cpython-313.pyc
|       |   |           measure_serializer.cpython-313.pyc
|       |   |           measure_series.cpython-313.pyc
|       |   |           sensor_serializer.cpython-313.pyc
|       |   |           __init__.cpython-313.pyc
|       |   |           
|       |   +---meta_data_file
|       |   |   |   coordinate.py
|       |   |   |   meta_data_file.py
|       |   |   |   variable.py
|       |   |   |   __init__.py
|       |   |   |   
|       |   |   \---__pycache__
|       |   |           coordinate.cpython-312.pyc
|       |   |           coordinate.cpython-313.pyc
|       |   |           meta_data_file.cpython-312.pyc
|       |   |           meta_data_file.cpython-313.pyc
|       |   |           variable.cpython-312.pyc
|       |   |           variable.cpython-313.pyc
|       |   |           __init__.cpython-312.pyc
|       |   |           __init__.cpython-313.pyc
|       |   |           
|       |   +---temporal
|       |   |   |   period.py
|       |   |   |   with_time.py
|       |   |   |   __init__.py
|       |   |   |   
|       |   |   \---__pycache__
|       |   |           period.cpython-313.pyc
|       |   |           with_time.cpython-313.pyc
|       |   |           __init__.cpython-313.pyc
|       |   |           
|       |   \---__pycache__
|       |           datafile.cpython-313.pyc
|       |           datafile_lifecycle.cpython-312.pyc
|       |           datafile_lifecycle.cpython-313.pyc
|       |           datafile_serializer.cpython-313.pyc
|       |           measure_query.cpython-313.pyc
|       |           sensor.cpython-313.pyc
|       |           task_status.cpython-312.pyc
|       |           workspace.cpython-313.pyc
|       |           __init__.cpython-312.pyc
|       |           __init__.cpython-313.pyc
|       |           
|       +---ports
|       |   |   data_file_repository.py
|       |   |   file_repository.py
|       |   |   measure_repository.py
|       |   |   sensor_repository.py
|       |   |   ws_repository.py
|       |   |   __init__.py
|       |   |   
|       |   \---__pycache__
|       |           data_file_repository.cpython-312.pyc
|       |           data_file_repository.cpython-313.pyc
|       |           file_repository.cpython-312.pyc
|       |           file_repository.cpython-313.pyc
|       |           measure_repository.cpython-312.pyc
|       |           measure_repository.cpython-313.pyc
|       |           sensor_repository.cpython-313.pyc
|       |           ws_repository.cpython-313.pyc
|       |           __init__.cpython-312.pyc
|       |           __init__.cpython-313.pyc
|       |           
|       +---services
|       |   |   data_file_creation_service.py
|       |   |   data_file_ingestion_service.py
|       |   |   data_file_messaging_service.py
|       |   |   data_file_upload_service.py
|       |   |   workspace_service.py
|       |   |   __init__.py
|       |   |   
|       |   \---__pycache__
|       |           data_file_creation_service.cpython-312.pyc
|       |           data_file_creation_service.cpython-313.pyc
|       |           data_file_ingestion_service.cpython-312.pyc
|       |           data_file_ingestion_service.cpython-313.pyc
|       |           data_file_messaging_service.cpython-312.pyc
|       |           data_file_messaging_service.cpython-313.pyc
|       |           data_file_upload_service.cpython-312.pyc
|       |           data_file_upload_service.cpython-313.pyc
|       |           workspace_service.cpython-313.pyc
|       |           __init__.cpython-312.pyc
|       |           __init__.cpython-313.pyc
|       |           
|       \---__pycache__
|               config.cpython-312.pyc
|               config.cpython-313.pyc
|               utils.cpython-313.pyc
|               __init__.cpython-312.pyc
|               __init__.cpython-313.pyc
|               
\---tests
    |   test_datafile_creation_service.py
    |   test_datafile_serialiser.py
    |   test_data_file.py
    |   test_measure_serialiser.py
    |   
    \---__pycache__
            test_datafile_creation_service.cpython-312.pyc
            test_datafile_creation_service.cpython-313.pyc
            test_datafile_serialiser.cpython-312.pyc
            test_datafile_serialiser.cpython-313.pyc
            test_data_file.cpython-312.pyc
            test_data_file.cpython-313.pyc
            test_measure_serialiser.cpython-312.pyc
            test_measure_serialiser.cpython-313.pyc
            
```
