from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.data_file.ports.data_file_repository import DataFileRepository
from sql_connector.model_mapping import ModelMapping
from sql_connector.sql_connection import SqlConnection
from sql_connector.sql_repository import SqlRepository

from sql_meteo_adapters.data_file_model import DataFileModel


class SqlDataFileRepository(
    SqlRepository[DataFile, DataFileModel],
    DataFileRepository,
):
    def __init__(self, connection: SqlConnection):
        super().__init__(connection, ModelMapping(DataFile, DataFileModel))
