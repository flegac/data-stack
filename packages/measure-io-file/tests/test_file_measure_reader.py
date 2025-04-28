from pathlib import Path

from measure_io_file.file_config import FileConfig
from measure_io_file.file_measure_reader import FileMeasureReader


def main():
    path = Path.home() / 'Documents' / 'Data' / 'Datasets'
    filepath = path / 'CDS-2025-01.grib'
    filepath = path / 'CDS-1983-10-22.nc'
    filepath = path / 'CDS-1983-10.nc'

    grib = FileConfig(
        path=path / 'CDS-hydro-2020-10-22.nc',
        variables=['precip']
    )

    reader = FileMeasureReader(grib)
    for measures in reader.read_all():
        max_value = measures.measures['value'].max()
        print(measures.sensor, measures.measures.head())


if __name__ == '__main__':
    main()
