from meteo_domain.core.repository import Repository
from meteo_domain.data_file.entities.datafile import DataFile


DataFileRepository = Repository[DataFile]
