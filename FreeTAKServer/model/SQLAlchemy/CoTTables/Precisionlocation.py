#######################################################
#
# Precisionlocation.py
# Python implementation of the Class Precisionlocation
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 9:41:37 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import String
from sqlalchemy.orm import relationship


class Precisionlocation(Base):
    # default constructor  def __init__(self):

    __tablename__ = "Precisionlocation"
    PrimaryKey = Column(ForeignKey("Detail.PrimaryKey"), primary_key=True)
    Detail = relationship("Detail", back_populates="precisionlocation")
    # TDB can be DTED0 or ???
    altsrc = Column(String)
    geopointsrc = Column(String)
