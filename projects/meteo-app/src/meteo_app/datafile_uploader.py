import asyncio
import datetime

from aa_common.constants import EXPORT_PATH
from meteo_app.wires.config import INI_FILE
from meteo_app.wires.services import Services
from meteo_app.workers.data_file_upload_worker import DataFileUploadWorker
from meteo_domain.entities.meta_data_file.coordinate import Coordinate
from meteo_domain.entities.meta_data_file.meta_data_file import MetaDataFile
from meteo_domain.entities.meta_data_file.variable import Variable
from meteo_domain.services.data_file_creation_service import DataFileCreationService


# filepath = DATASET_ROOT_PATH / "CDS-2025-01.grib"
# filepath = DATASET_ROOT_PATH / "CDS-1983-10-22.nc"
# filepath = DATASET_ROOT_PATH / "CDS-1983-10.nc"
# filepath = DATASET_ROOT_PATH / "CDS-hydro-2020-10-22.nc"


def main():
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())
    services.wire(modules=[__name__])

    filepath = EXPORT_PATH / "dummy.grib"
    now = datetime.datetime.now(datetime.UTC)
    DataFileCreationService().randomize(
        MetaDataFile(
            coords=[
                Coordinate.interval(
                    "time",
                    start=now,
                    end=now + datetime.timedelta(hours=24),
                    steps=24,
                ),
                Coordinate.interval("latitude", start=0, end=180, steps=3),
                Coordinate.interval("longitude", start=0, end=360, steps=6),
            ],
            variables=[Variable("temperature", ["time", "latitude", "longitude"])],
        ),
        filepath,
    )

    worker = DataFileUploadWorker(datafile_path=filepath)

    asyncio.run(worker.run())


if __name__ == "__main__":
    main()
