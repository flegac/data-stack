```
aa-common v0.1.0
├── dependency-injector v4.46.0
└── loguru v0.7.3
black v25.1.0
├── click v8.1.8
├── mypy-extensions v1.1.0
├── packaging v25.0
├── pathspec v0.12.1
└── platformdirs v4.3.7
boto3 v1.37.3
├── botocore v1.37.3
│   ├── jmespath v1.0.1
│   ├── python-dateutil v2.9.0.post0
│   │   └── six v1.17.0
│   └── urllib3 v2.4.0
├── jmespath v1.0.1
└── s3transfer v0.11.3
    └── botocore v1.37.3 (*)
celery v5.5.2
├── billiard v4.2.1
├── click v8.1.8
├── click-didyoumean v0.3.1
│   └── click v8.1.8
├── click-plugins v1.1.1
│   └── click v8.1.8
├── click-repl v0.3.0
│   ├── click v8.1.8
│   └── prompt-toolkit v3.0.51
│       └── wcwidth v0.2.13
├── kombu v5.5.3
│   ├── amqp v5.3.1
│   │   └── vine v5.1.0
│   ├── tzdata v2025.2
│   └── vine v5.1.0
├── python-dateutil v2.9.0.post0 (*)
└── vine v5.1.0
celery-connector v0.1.0
└── redis v6.0.0
coverage v7.8.0
cryptography v44.0.3
└── cffi v1.17.1
    └── pycparser v2.22
data-file-repository-pg v0.1.0
├── meteo-domain v0.1.0
│   ├── h5netcdf v1.6.1
│   │   ├── h5py v3.13.0
│   │   │   └── numpy v2.2.5
│   │   └── packaging v25.0
│   └── xarray v2025.4.0
│       ├── numpy v2.2.5
│       ├── packaging v25.0
│       └── pandas v2.2.3
│           ├── numpy v2.2.5
│           ├── python-dateutil v2.9.0.post0 (*)
│           ├── pytz v2025.2
│           └── tzdata v2025.2
└── pg-connector v0.1.0
    ├── asyncpg v0.30.0
    ├── databases v0.9.0
    │   └── sqlalchemy v2.0.40
    │       ├── greenlet v3.2.1
    │       └── typing-extensions v4.13.2
    └── sqlalchemy v2.0.40 (*)
file-repository-posix v0.1.0
└── meteo-domain v0.1.0 (*)
file-repository-s3 v0.1.0
├── meteo-domain v0.1.0 (*)
└── s3-connector v0.1.0
    ├── aioboto3 v14.2.0
    │   ├── aiobotocore v2.22.0
    │   │   ├── aiohttp v3.11.18
    │   │   │   ├── aiohappyeyeballs v2.6.1
    │   │   │   ├── aiosignal v1.3.2
    │   │   │   │   └── frozenlist v1.6.0
    │   │   │   ├── attrs v25.3.0
    │   │   │   ├── frozenlist v1.6.0
    │   │   │   ├── multidict v6.4.3
    │   │   │   ├── propcache v0.3.1
    │   │   │   └── yarl v1.20.0
    │   │   │       ├── idna v3.10
    │   │   │       ├── multidict v6.4.3
    │   │   │       └── propcache v0.3.1
    │   │   ├── aioitertools v0.12.0
    │   │   ├── botocore v1.37.3 (*)
    │   │   ├── jmespath v1.0.1
    │   │   ├── multidict v6.4.3
    │   │   ├── python-dateutil v2.9.0.post0 (*)
    │   │   └── wrapt v1.17.2
    │   └── aiofiles v24.1.0
    └── aiohappyeyeballs v2.6.1
flake8 v7.2.0
├── mccabe v0.7.0
├── pycodestyle v2.13.0
└── pyflakes v3.3.2
httptools v0.6.4
httpx v0.28.1
├── anyio v4.9.0
│   ├── idna v3.10
│   ├── sniffio v1.3.1
│   └── typing-extensions v4.13.2
├── certifi v2025.4.26
├── httpcore v1.0.9
│   ├── certifi v2025.4.26
│   └── h11 v0.16.0
└── idna v3.10
measure-repository-datafile v0.1.0
└── meteo-domain v0.1.0 (*)
measure-repository-influxdb v0.1.0
├── influxdb-connector v0.1.0
│   └── influxdb-client v1.48.0
│       ├── certifi v2025.4.26
│       ├── python-dateutil v2.9.0.post0 (*)
│       ├── reactivex v4.0.4
│       │   └── typing-extensions v4.13.2
│       ├── setuptools v80.3.1
│       └── urllib3 v2.4.0
└── meteo-domain v0.1.0 (*)
measure-repository-openmeteo v0.1.0
├── meteo-domain v0.1.0 (*)
├── numpy v2.2.5
├── openmeteo-requests v1.4.0
│   ├── openmeteo-sdk v1.20.0
│   │   └── flatbuffers v25.2.10
│   └── requests v2.32.3
│       ├── certifi v2025.4.26
│       ├── charset-normalizer v3.4.2
│       ├── idna v3.10
│       └── urllib3 v2.4.0
├── pandas v2.2.3 (*)
├── requests-cache v1.2.1
│   ├── attrs v25.3.0
│   ├── cattrs v24.1.3
│   │   └── attrs v25.3.0
│   ├── platformdirs v4.3.7
│   ├── requests v2.32.3 (*)
│   ├── url-normalize v2.2.1
│   │   └── idna v3.10
│   └── urllib3 v2.4.0
└── retry-requests v2.0.0
    ├── requests v2.32.3 (*)
    └── urllib3 v2.4.0
message-queue v0.1.0
message-queue-kafka v0.1.0
├── kafka-connector v0.1.0
│   ├── aiohttp v3.11.18 (*)
│   ├── aiohttp-cors v0.8.1
│   │   └── aiohttp v3.11.18 (*)
│   ├── aiokafka v0.12.0
│   │   ├── async-timeout v5.0.1
│   │   ├── packaging v25.0
│   │   └── typing-extensions v4.13.2
│   ├── aiosignal v1.3.2 (*)
│   ├── async-timeout v5.0.1
│   └── kafka-python-ng v2.2.3
└── meteo-domain v0.1.0 (*)
meteo-app v0.1.0
├── cfgrib v0.9.15.0
│   ├── attrs v25.3.0
│   ├── click v8.1.8
│   ├── eccodes v2.41.0
│   │   ├── attrs v25.3.0
│   │   ├── cffi v1.17.1 (*)
│   │   ├── findlibs v0.1.1
│   │   └── numpy v2.2.5
│   └── numpy v2.2.5
├── fastapi v0.115.12
│   ├── pydantic v2.11.4
│   │   ├── annotated-types v0.7.0
│   │   ├── pydantic-core v2.33.2
│   │   │   └── typing-extensions v4.13.2
│   │   ├── typing-extensions v4.13.2
│   │   └── typing-inspection v0.4.0
│   │       └── typing-extensions v4.13.2
│   ├── starlette v0.46.2
│   │   └── anyio v4.9.0 (*)
│   └── typing-extensions v4.13.2
├── python-multipart v0.0.20
├── scipy v1.15.2
│   └── numpy v2.2.5
└── uvicorn v0.34.2
    ├── click v8.1.8
    └── h11 v0.16.0
meteo-backend v1.0.0
├── dependency-injector v4.46.0
├── fastapi v0.115.12 (*)
├── meteo-domain v0.1.0 (*)
├── pydantic v2.11.4 (*)
├── pydantic-settings v2.9.1
│   ├── pydantic v2.11.4 (*)
│   ├── python-dotenv v1.1.0
│   └── typing-inspection v0.4.0 (*)
├── python-jose v3.4.0
│   ├── ecdsa v0.19.1
│   │   └── six v1.17.0
│   ├── pyasn1 v0.4.8
│   └── rsa v4.9.1
│       └── pyasn1 v0.4.8
├── python-multipart v0.0.20
└── uvicorn v0.34.2 (*)
pdoc v15.0.3
├── jinja2 v3.1.6
│   └── markupsafe v3.0.2
├── markupsafe v3.0.2
└── pygments v2.19.1
pre-commit v4.2.0
├── cfgv v3.4.0
├── identify v2.6.10
├── nodeenv v1.9.1
├── pyyaml v6.0.2
└── virtualenv v20.31.1
    ├── distlib v0.3.9
    ├── filelock v3.18.0
    └── platformdirs v4.3.7
pydeps v3.0.1
└── stdlib-list v0.11.1
pylint v3.3.7
├── astroid v3.3.9
├── dill v0.4.0
├── dill v0.4.0
├── isort v6.0.1
├── mccabe v0.7.0
├── platformdirs v4.3.7
└── tomlkit v0.13.2
radon v6.0.1
├── colorama v0.4.6
└── mando v0.7.1
    └── six v1.17.0
ruff v0.11.8
uvloop v0.21.0
watchfiles v1.0.5
└── anyio v4.9.0 (*)
websockets v15.0.1
(*) Package tree already displayed
```
