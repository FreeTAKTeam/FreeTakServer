#######################################################
#
# dest.py
# Python implementation of the Class dest
# Generated by Enterprise Architect
# Created on:      26-Sep-2020 9:41:48 PM
# Original author: natha
#
#######################################################
from sqlalchemy import Column, ForeignKey
from FreeTAKServer.model.SQLAlchemy.Root import Base
from sqlalchemy import Integer
from sqlalchemy import String


class Dest(Base):
    # default constructor  def __init__(self):

    # the call sign of the destination
    __tablename__ = "Dest"
    PrimaryKey = Column(Integer, primary_key=True, autoincrement=True)
    OwnerPrimaryKey = Column(String, ForeignKey("Marti.PrimaryKey"))
    callsign = Column(String)
