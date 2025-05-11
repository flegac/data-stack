from unittest import TestCase

from aa_common.constants import DATASET_ROOT_PATH, EXPORT_PATH
from aa_common.logger import logger
from meteo_domain.entities.datafile import DataFile
from meteo_domain.services.metadatafile_service import MetadataFileService


class TestDataFile(TestCase):
    def setUp(self):
        EXPORT_PATH.mkdir(parents=True, exist_ok=True)

    def test_it(self):

        service = MetadataFileService()

        grib = DataFile.from_file(
            path=DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc",
        )
        data = service.load_raw_data(grib)
        logger.info(data)

        data.to_netcdf(EXPORT_PATH / "data.h5")
        data.to_dataframe().to_csv(EXPORT_PATH / "data.csv")

        xxx = DataFile.from_file(EXPORT_PATH / "data.h5")
        xxx_data = service.load_raw_data(xxx)

        logger.info(xxx_data)
