# Data-stack

Small project to experiment with different data oriented libraries.

## Setup

```bash
uv venv
uv sync --all-packages 
```

## Architecture

The project is composed of several packages:

- `temperature-datasource`: a simple package that provides a function to get the temperature in a given city
- `temperature-repository`: a simple package that provides a function to get the temperature in a given city
- `meteo-app`: a simple package that provides a function to get the temperature in a given city
- `meteo-backend`: a simple package that provides a function to get the temperature in a given city

## Stack

Message brokers:

- Kafka
- RabbitMQ

- https://injector.readthedocs.io/en/latest/