from itertools import islice
from pathlib import Path

from data_file_repository.data_file import DataFile
from measure_io_datafile.datafile_measure_reader import DataFileMeasureReader


def main():
    path = Path.home() / 'Documents' / 'Data' / 'Datasets'
    filepath = path / 'CDS-2025-01.grib'
    filepath = path / 'CDS-1983-10-22.nc'
    filepath = path / 'CDS-1983-10.nc'

    grib = DataFile.from_file(
        path=path / 'CDS-hydro-2020-10-22.nc',
    )

    reader = DataFileMeasureReader(grib)
    provider = islice(reader.read_all(), 5)

    for measures in provider:
        max_value = measures.measures['value'].max()
        print(measures.sensor, measures.measures.head())


if __name__ == '__main__':
    main()
