import xarray as xr

from meteo_domain.entities.datafile import DataFile
from meteo_domain.entities.meta_data_file.coordinate import Coordinate
from meteo_domain.entities.meta_data_file.meta_data_file import MetaDataFile
from meteo_domain.entities.meta_data_file.variable import Variable


class MetadataFileService:

    # TODO: xarray should not be exposed
    def load_raw_data(self, item: DataFile) -> xr.Dataset:
        return xr.open_dataset(item.local_path)

    def load_from_datafile(self, item: DataFile) -> MetaDataFile:
        raw = self.load_raw_data(item)

        return MetaDataFile(
            coords=[Coordinate(str(k), list(v)) for k, v in raw.coords.items()],
            variables=[
                Variable(str(k), list(v.coords.keys()))
                for k, v in raw.data_vars.items()
                if "bounds" not in k
            ],
            metadata=raw.attrs,
        )
