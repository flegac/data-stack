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
boto3 v1.37.1
├── botocore v1.37.1
│   ├── jmespath v1.0.1
│   ├── python-dateutil v2.9.0.post0
│   │   └── six v1.17.0
│   └── urllib3 v2.4.0
├── jmespath v1.0.1
└── s3transfer v0.11.3
    └── botocore v1.37.1 (*)
coverage v7.8.0
data-file-repository-pg v0.1.0
├── asyncpg v0.30.0
├── databases v0.9.0
│   └── sqlalchemy v2.0.40
│       ├── greenlet v3.2.1
│       └── typing-extensions v4.13.2
└── sqlalchemy v2.0.40 (*)
file-repository-posix v0.1.0
file-repository-s3 v0.1.0
├── aioboto3 v14.1.0
│   ├── aiobotocore v2.21.1
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
│   │   ├── botocore v1.37.1 (*)
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
measure-repository-datafile v0.1.0
measure-repository-influxdb v0.1.0
└── influxdb-client v1.48.0
    ├── certifi v2025.4.26
    ├── python-dateutil v2.9.0.post0 (*)
    ├── reactivex v4.0.4
    │   └── typing-extensions v4.13.2
    ├── setuptools v80.1.0
    └── urllib3 v2.4.0
measure-repository-openmeteo v0.1.0
├── numpy v2.2.5
├── openmeteo-requests v1.4.0
│   ├── openmeteo-sdk v1.20.0
│   │   └── flatbuffers v25.2.10
│   └── requests v2.32.3
│       ├── certifi v2025.4.26
│       ├── charset-normalizer v3.4.2
│       ├── idna v3.10
│       └── urllib3 v2.4.0
├── pandas v2.2.3
│   ├── numpy v2.2.5
│   ├── python-dateutil v2.9.0.post0 (*)
│   ├── pytz v2025.2
│   └── tzdata v2025.2
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
├── aiohttp v3.11.18 (*)
├── aiohttp-cors v0.8.1
│   └── aiohttp v3.11.18 (*)
├── aiokafka v0.12.0
│   ├── async-timeout v5.0.1
│   ├── packaging v25.0
│   └── typing-extensions v4.13.2
├── aiosignal v1.3.2 (*)
├── async-timeout v5.0.1
├── confluent-kafka v2.10.0
└── kafka-python-ng v2.2.3
meteo-app v0.1.0
├── cfgrib v0.9.15.0
│   ├── attrs v25.3.0
│   ├── click v8.1.8
│   ├── eccodes v2.41.0
│   │   ├── attrs v25.3.0
│   │   ├── cffi v1.17.1
│   │   │   └── pycparser v2.22
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
│   │   └── anyio v4.9.0
│   │       ├── idna v3.10
│   │       ├── sniffio v1.3.1
│   │       └── typing-extensions v4.13.2
│   └── typing-extensions v4.13.2
├── python-multipart v0.0.20
├── scipy v1.15.2
│   └── numpy v2.2.5
└── uvicorn v0.34.2
    ├── click v8.1.8
    └── h11 v0.16.0
meteo-measures v0.1.0
├── h5netcdf v1.6.1
│   ├── h5py v3.13.0
│   │   └── numpy v2.2.5
│   └── packaging v25.0
└── xarray v2025.4.0
    ├── numpy v2.2.5
    ├── packaging v25.0
    └── pandas v2.2.3 (*)
pre-commit v4.2.0
├── cfgv v3.4.0
├── identify v2.6.10
├── nodeenv v1.9.1
├── pyyaml v6.0.2
└── virtualenv v20.30.0
    ├── distlib v0.3.9
    ├── filelock v3.18.0
    └── platformdirs v4.3.7
pydeps v3.0.1
└── stdlib-list v0.11.1
pylint v3.3.6
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
(*) Package tree already displayed
```
