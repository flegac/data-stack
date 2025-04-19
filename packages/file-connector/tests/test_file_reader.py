from pathlib import Path
from unittest import TestCase

from file_connector.file_config import FileConfig

ROOT_PATH = Path.home() / 'Documents' / 'Data' / 'Datasets'


class TestFileReader(TestCase):

    def test_grib(self):
        config = FileConfig(
            path=ROOT_PATH / 'CDS-2025-01.grib',
            variables=['t2m', 'sp']
        )
        print(config.raw)

    def test_precip(self):
        config = FileConfig(
            path=ROOT_PATH / 'CDS-hydro-2020-10-22.nc',
            variables=['precip']
        )
        print(config.raw)

    def test_ndf5(self):
        for path in [
            ROOT_PATH / 'CDS-1983-10-22.nc',
            ROOT_PATH / 'CDS-1983-10.nc',
        ]:
            config = FileConfig(
                path=path,
                variables=['t2m']
            )
            print(config.raw)

        # reader = GribMeasureReader(config)
        # reader.show_config()
