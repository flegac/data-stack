```
Structure du dossier
Le num�ro de s�rie du volume est C4D9-4B96
C:\USERS\FLO\DOCUMENTS\WORKSPACE\DATA-STACK\PROJECTS\AA-COMMON
|   .python-version
|   pyproject.toml
|   README.md
|   
+---src
|   \---aa_common
|       |   constants.py
|       |   logger.py
|       |   memory.py
|       |   __init__.py
|       |   
|       +---mq
|       |   |   memory_mq_backend.py
|       |   |   mq_backend.py
|       |   |   mq_backend_checker.py
|       |   |   mq_consumer.py
|       |   |   mq_producer.py
|       |   |   mq_topic.py
|       |   |   serializer.py
|       |   |   __init__.py
|       |   |   
|       |   \---__pycache__
|       |           mq_backend.cpython-313.pyc
|       |           mq_backend_checker.cpython-313.pyc
|       |           mq_consumer.cpython-313.pyc
|       |           mq_producer.cpython-313.pyc
|       |           mq_topic.cpython-313.pyc
|       |           serializer.cpython-313.pyc
|       |           __init__.cpython-313.pyc
|       |           
|       +---repo
|       |   |   repository.py
|       |   |   repository_checker.py
|       |   |   __init__.py
|       |   |   
|       |   \---__pycache__
|       |           repository.cpython-313.pyc
|       |           repository_checker.cpython-313.pyc
|       |           __init__.cpython-313.pyc
|       |           
|       \---__pycache__
|               constants.cpython-312.pyc
|               constants.cpython-313.pyc
|               logger.cpython-312.pyc
|               logger.cpython-313.pyc
|               memory.cpython-313.pyc
|               __init__.cpython-312.pyc
|               __init__.cpython-313.pyc
|               
\---tests
        test_dependency_injector.py
        test_memory_mq.py
        
```
