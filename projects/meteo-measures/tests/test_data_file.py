from pathlib import Path
from unittest import TestCase

from aa_common.constants import DATASET_ROOT_PATH
from meteo_measures.domain.entities.data_file import DataFile

EXPORT_PATH = Path.cwd() / "exports"
EXPORT_PATH.mkdir(parents=True, exist_ok=True)


class TestDataFile(TestCase):
    def test_it(self):
        grib = DataFile.from_file(
            path=DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        )

        data = grib.raw
        print(data)

        data.to_netcdf(EXPORT_PATH / "data.h5")
        data.to_dataframe().to_csv(EXPORT_PATH / "data.csv")

        xxx = DataFile.from_file(EXPORT_PATH / "data.h5")
        print(xxx.raw)
