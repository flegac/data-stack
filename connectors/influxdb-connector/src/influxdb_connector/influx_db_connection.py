from functools import cached_property
from typing import Any

from influxdb_client import InfluxDBClient
from influxdb_client.client.flux_table import TableList
from influxdb_client.client.write_api import SYNCHRONOUS
from loguru import logger

from influxdb_connector.influxdb_config import InfluxDBConfig


class InfluxDbConnection:
    def __init__(self, config: InfluxDBConfig):
        self.config = config

    def write(self, record: Any):
        return self.write_api.write(
            bucket=self.config.bucket,
            org=self.config.org,
            record=record,
        )

    def query(self, flux_query: str) -> TableList:
        logger.debug(f"flux:\n{flux_query}")
        return self.query_api.query(flux_query, org=self.config.org)

    @cached_property
    def client(self):
        return InfluxDBClient(
            url=self.config.url,
            token=self.config.token,
            org=self.config.org,
        )

    @property
    def write_api(self):
        return self.client.write_api(write_options=SYNCHRONOUS)

    @property
    def query_api(self):
        return self.client.query_api()

    def close(self):
        if hasattr(self, "client"):
            self.client.close()
            del self.__dict__["client"]
