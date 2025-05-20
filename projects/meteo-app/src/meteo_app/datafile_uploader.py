import asyncio
import datetime

from meteo_domain.config import EXPORT_PATH
from meteo_domain.datafile_ingestion.entities.coordinate import Coordinate
from meteo_domain.datafile_ingestion.entities.meta_data_file import MetaDataFile
from meteo_domain.datafile_ingestion.entities.variable import Variable
from meteo_domain.datafile_ingestion.entities.workspace import Workspace

from meteo_app.wires.config import INI_FILE
from meteo_app.wires.services import Services


def main():
    services = Services()
    services.repositories.config.config.from_ini(INI_FILE.absolute())
    services.wire(modules=[__name__])

    filepath = EXPORT_PATH / "dummy.grib"
    now = datetime.datetime.now(datetime.UTC)
    services.datafile_service.randomize(
        MetaDataFile(
            coords=[
                Coordinate.interval(
                    "times",
                    start=now,
                    end=now + datetime.timedelta(hours=24),
                    steps=24,
                ),
                Coordinate.interval("latitude", start=0, end=180, steps=3),
                Coordinate.interval("longitude", start=0, end=360, steps=6),
            ],
            variables=[Variable("temperature", ["times", "latitude", "longitude"])],
        ),
        filepath,
    )

    service = services.datafile_service()

    asyncio.run(
        service.upload_single(
            ws=Workspace(uid="default"),
            path=filepath,
        )
    )


if __name__ == "__main__":
    main()
