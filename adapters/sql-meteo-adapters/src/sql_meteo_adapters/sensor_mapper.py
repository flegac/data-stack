from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.sensor.entities.sensor import Sensor
from meteo_domain.workspace.entities.workspace import Workspace
from sql_connector.model_mapper import ModelMapper
from sql_connector.patches.location_patch import (
    LocationPatch,
)
from sql_meteo_adapters.models import SensorModel, WorkspaceModel, DataFileModel

SensorMapper = ModelMapper(Sensor, SensorModel, patches=[LocationPatch()])
WorkspaceMapper = ModelMapper(Workspace, WorkspaceModel, patches=[LocationPatch()])
DataFileMapper = ModelMapper(DataFile, DataFileModel, patches=[LocationPatch()])
