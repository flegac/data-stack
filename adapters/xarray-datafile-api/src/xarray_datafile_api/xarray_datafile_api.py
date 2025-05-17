import datetime
from pathlib import Path
from typing import override

import numpy as np
import xarray as xr

from meteo_domain.core.logger import logger
from meteo_domain.data_file.entities.datafile import DataFile
from meteo_domain.data_file.entities.meta_data_file import MetaDataFile
from meteo_domain.data_file.entities.metadata.coordinate import Coordinate
from meteo_domain.data_file.entities.metadata.variable import Variable
from meteo_domain.ports.datafile_api import DatafileAPI


class XarrayDatafileAPI(DatafileAPI[xr.Dataset]):
    @override
    def load_raw_data(self, item: DataFile) -> xr.Dataset:
        return xr.open_dataset(item.local_path)

    @override
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

    @override
    def randomize(self, metadata_file: MetaDataFile, output_file: Path) -> DataFile:
        logger.info(f"output: {output_file}\n{metadata_file}")

        metadata_file.check_coords()
        ds = xr.Dataset(
            attrs=metadata_file.metadata,
            coords={_.name: _.values for _ in metadata_file.coords},
            data_vars={
                var.name: (
                    var.coords,
                    np.random.random(
                        tuple(metadata_file.coord_sizes[_] for _ in var.coords)
                    ),
                )
                for var in metadata_file.variables
            },
        )
        return _create_from_xarray(ds, output_file)


def _create_from_xarray(ds: xr.Dataset, output_file: Path):
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Conversion des coordonnées datetime en np.datetime64
    for coord_name, coord in ds.coords.items():
        if any(isinstance(value, datetime.datetime) for value in coord.values):
            ds[coord_name] = coord.astype("datetime64[ns]")

    ds.to_netcdf(output_file, engine="h5netcdf")
    return DataFile.from_file(output_file)
