from sqlalchemy import Column, ForeignKey, String
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy.orm import relationship
from FreeTAKServer.model.SQLAlchemy.CoTTables import Connectionentry

class _Video(Base):
    __tablename__ = "_Video"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Connectionentry = relationship("Connectionentry", uselist=False, cascade="all, delete")
    Detail = relationship("Detail", back_populates="_video")
    sensor = Column(String(100))
    spi = Column(String(100))
    url = Column(String(100))