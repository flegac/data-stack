from geoalchemy2 import Geometry
from sqlalchemy import Column, String, Date, func
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class SensorModel(Base):
    __tablename__ = "sensors"
    uid = Column(String, primary_key=True)
    creation_date = Column(Date, server_default=func.now())
    last_update_date = Column(Date, server_default=func.now())
    workspace_id = Column(String)

    type = Column(String, index=True, nullable=False)
    location = Column(Geometry("POINT", srid=4326), index=True, nullable=False)
