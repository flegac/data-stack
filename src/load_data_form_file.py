from pathlib import Path

from grib_connector.grib_config import GribConfig
from grib_connector.grib_measure_reader import GribMeasureReader


def main():
    path = Path.home() / 'Documents' / 'Data' / 'Datasets'
    filepath = path / 'CDS-2025-01.grib'
    filepath = path / 'CDS-1983-10-22.nc'
    filepath = path / 'CDS-1983-10.nc'

    grib = GribConfig(
        path=path / 'CDS-hydro-2020-10-22.nc',
        variable_name='precip'
    )

    reader = GribMeasureReader(grib)
    for measures in reader.read_all():
        max_value = measures.measures['value'].max()
        print(measures.sensor, measures.measures.head())


if __name__ == '__main__':
    main()
