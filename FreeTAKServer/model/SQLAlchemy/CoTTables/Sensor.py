from sqlalchemy import Column, ForeignKey, String
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy.orm import relationship


class Sensor(Base):

    __tablename__ = 'Sensor'
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="sensor")
    elevation = Column(String(100))
    vfov = Column(String(100))
    north = Column(String(100))
    roll = Column(String(100))
    range = Column(String(100))
    azimuth = Column(String(100))
    model = Column(String(100))
    fov = Column(String(100))
    type = Column(String(100))
    version = Column(String(100))